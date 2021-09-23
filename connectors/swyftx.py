import logging
import pprint
import time
import typing
import json
import datetime
from creds.creds import creds
from models.models import *
import requests

logger = logging.getLogger()


class SwyftxClient:
    def __init__(self, testnet: bool, public_key: str):
        self._data = {'apiKey': public_key, 'Content-Type': 'application/json'}

        if testnet:
            self._base_url = 'https://api.demo.swyftx.com.au'
            self._token = creds['demoPrivateKey']
        else:
            self._base_url = 'https://api.swyftx.com.au'

            def _retrieve_jwt():
                # Generates a jwt that will be active for 1 week with the permissions associated with API Key
                response = requests.post(self._base_url + '/auth/refresh/', data=self._data)

                if response.status_code == 200:
                    return response.json()['accessToken']
                else:
                    logger.error("Error whilst making request for JWT: %s (error code %s)",
                                 response.json(), response.status_code)
                    return None

            self._token = _retrieve_jwt()

        self.prices = dict()
        self.orders = dict()
        self._header = {'Content-Type': 'application/json',
                       'Authorization': 'Bearer ' + self._token}

        self.assets = self.get_assets()
        self.balances = self.get_balance()

        logger.info("Swyftx Client successfully initialized")

    def _make_request(self, method, endpoint, data, header):
        if method == "GET":
            response = requests.get(self._base_url + endpoint, params=data, headers=self._header)
        elif method == "POST":
            response = requests.post(self._base_url + endpoint, data=data, headers=self._header)
        elif method == "DELETE":
            response = requests.delete(self._base_url + endpoint, data=data, headers=self._header)
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error whilst making %s request to %s: %s (error code %s)",
                         method, endpoint, response.json(), response.status_code)
            return None

    # Data methods that call public endpoints
    def get_assets(self) -> typing.Dict[str, Asset]:
        """Retrieves all the assets currently listed on Swyftx, including basic
           information about the market cap, 24hr volume, and IDs"""
        asset_attributes = dict()
        response = self._make_request("GET", "/markets/assets/", None, None)
        if response is not None:
            for asset in response:
                if asset['tradable'] == 1 and asset['buyDisabled'] == 0 and asset['assetType'] == 2:
                    asset_attributes[asset['code']] = Asset(asset)
        return asset_attributes

    def get_historical_candles(self, symbol, resolution, start, end):  # TBD: implement start and end date
        """Retrieves the historical OHLC data against AUD for the given symbol, at the specified resolution.
           Currently pulls all data from the last 24 hours"""
        data = dict()
        data['baseAsset'] = "AUD"
        data['secondaryAsset'] = symbol
        data['timeStart'] = 1000 * int(datetime.datetime.utcnow().timestamp()) - 86400000
        data['timeEnd'] = 1000 * int(datetime.datetime.utcnow().timestamp())
        data['resolution'] = resolution
        data['limit'] = 1000

        raw_candles = self._make_request("GET", "/charts/getBars/AUD/" + symbol + "/ask/", data, None)['candles']
        pprint.pprint(raw_candles)
        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                # pprint.pprint(c)
                candles.append([float(c['close']), float(c['high']), float(c['low']), float(c['open']),
                                c['time'], c['volume']])
        return candles

    def get_bid_ask(self, symbol):
        """Given an asset, return the current bid-ask"""
        bid_ask_info = self._make_request("GET", "/markets/info/basic/"+symbol+"/", data=None, header=None)[0]
        # pprint.pprint(bid_ask_info[0]['buy'])
        asset_data = dict()
        asset_data['symbol'] = symbol

        if bid_ask_info is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(bid_ask_info['buy']), 'ask': float(bid_ask_info['sell'])}
            else:
                self.prices[symbol]['bid'] = float(bid_ask_info['buy'])
                self.prices[symbol]['ask'] = float(bid_ask_info['sell'])

        return self.prices[symbol]

    # Methods that interact with a private endpoint
    def get_balance(self) -> typing.Dict[str, Balance]:
        """Returns the balances in an account for each asset
        Note: returns the assetId, not the asset Name"""
        balances = dict()
        response = self._make_request("GET", "/user/balance/", None, self._header)

        if response is not None:
            for a in self.assets.values():
                for b in response:
                    if a.assetId == b['assetId']:
                        b['symbol'] = a.symbol
                        balances[a.symbol] = Balance(b)

        # pprint.pprint(balances)
        return balances

    def place_order(self, primary, secondary, quantity, asset_quantity, order_type, trigger):
        """Places an order based on the input parameters. Note the following for orderType:
           1: Market Buy
           2: Market Sell
           3: Limit Buy : Buys secondary asset when price DROPS to trigger price
           4: Limit Sell : Sells secondary asset when price RISES to trigger price
           5: Stop Limit Buy : Buys secondary asset if price RISES to trigger price
           6: Stop Limit Sell : Sells secondary asset if price DROPS to trigger price
           8: Dust Sell
            Note for Trigger: Price to trigger order at.
                For limit and stop buy orders (orderType: LIMIT_BUY,STOP_LIMIT_BUY), price is primary per secondary.
                e.g. 52000 USD/BTC -> trigger: 52000.
                For limit and stop sell orders (orderType: LIMIT_SELL,STOP_LIMIT_SELL), price is secondary per primary.
                e.g. 1 BTC / 52000 USD -> trigger: 0.0000192307.
        """
        order_data = dict()
        order_data["primary"] = primary  # "USD"
        order_data["secondary"] = secondary  # "BTC"
        order_data["quantity"] = quantity  # "1000"
        order_data["assetQuantity"] = asset_quantity  # "USD"
        order_data["orderType"] = order_type  # 0
        order_data["trigger"] = trigger  # "52000"

        place_order = self._make_request("POST", "/orders/", data=json.dumps(order_data), header=self._header)
        # pprint.pprint(place_order)
        # TODO: Work out if the order info can be returned outside of prod mode, demo seems to just return
        #       the order orderUuid
        # if place_order is not None:
        #     if place_order['orderUuid'] not in self.orders:
        #         self.orders[place_order['orderUuid']] = {'order_id': place_order['orderUuid'],
        #                                                  'order_info': place_order['order']}
        #     else:
        #         self.orders[place_order['orderUuid']]['order_id'] = place_order['orderUuid']
        #         self.orders[place_order['orderUuid']]['order_info'] = place_order['order']
        # #pprint.pprint(self.orders[place_order['orderUuid']])
        return None  # self.orders[place_order['orderUuid']]

    def cancel_order(self, order_id):
        cancellation = self._make_request("DELETE", "/orders/" + order_id + "/", data=None, header=self._header)
        print(cancellation)
        if cancellation.status_code == 200:
            logger.info("INFO: Order %s was successfully Cancelled", order_id)
        return None

    def get_order_status(self, order_id):
        """Returns the """
        order_status = self._make_request("GET", "/orders/byId/" + order_id + "/", data=None, header=self._header)
        # TODO: cherry pick the data that's most relevant
        # order_details = dict()
        #
        # if order_status is not None:
        #     order_details['order_id'] = order_status['orderUuid']
        #     order_details['order_status'] = ...
        return order_status

    def get_all_orders(self, symbol):  # TODO: Implement logic to subset by order status / value
        all_orders = self._make_request("GET", "/orders/" + symbol, data=None, header=self._header)
        return all_orders

