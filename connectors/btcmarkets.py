import logging
import pprint
import time
import json
import datetime
import requests
import websocket
import json
import threading

logger = logging.getLogger()


class BTCMarketsClient:
    def __init__(self, public_key, private_key):
        self.base_url = 'https://api.btcmarkets.net/v3/markets'
        self.wss_url = 'wss://socket.btcmarkets.net/v2'
        self.public_key = public_key
        self.private_key = private_key
        self.ws = None
        self.prices = dict()

        t = threading.Thread(target=self.start_ws)
        t.start()

        logger.info("BTCMarkets Client successfully initialized")

    def start_ws(self):
        self.ws = websocket.WebSocketApp(self.wss_url, on_open=self.on_open, on_message=self.on_message,
                                         on_error=self.on_error, on_close=self.on_close)
        self.ws.run_forever()

    def on_open(self, ws):
        logger.info("BTCMarkets connection opened")
        self.subscribe_channel('ETH-AUD', ['tick', 'heartbeat'])

    def on_close(self, ws):
        logger.warning("BTCMarkets connection opened")

    def on_error(self, ws, msg):
        logger.error("BTCMarkets connection error: %s", msg)

    def on_message(self, ws, msg):
        data = json.loads(msg)
        if "messageType" in data:
            if data['messageType'] == "tick":
                if data['marketId'] not in self.prices:
                    self.prices[data['marketId']] = {'bid': float(data['bestBid']), 'ask': float(data['bestAsk'])}
                else:
                    self.prices[data['marketId']]['bid'] = float(data['bestBid'])
                    self.prices[data['marketId']]['ask'] = float(data['bestAsk'])
                print(self.prices)

    def subscribe_channel(self, symbol, channels):
        data = {'messageType': 'subscribe', 'marketIds': [symbol], 'channels': channels}
        self.ws.send(json.dumps(data))

