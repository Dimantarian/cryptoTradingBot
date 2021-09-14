import logging
import pprint
import time
import json
import datetime

import requests

logger = logging.getLogger()


class swyftxClient:
    def __init__(self, testnet,public_key):
        self.data = {'apiKey': public_key, 'Content-Type': 'application/json'}

        if testnet:
            self.base_url = 'https://api.demo.swyftx.com.au'
            self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJrVTRRelF6TlRaQk5rTkNORGsyTnpnME9EYzNOVEZGTWpaRE9USTRNalV6UXpVNE1UUkROUSJ9.eyJodHRwczovL3N3eWZ0eC5jb20uYXUvLWp0aSI6ImY5ZTQ5OGQ0LTEzMmItNGE4NS1iZTEzLTdjNTVmMGRmN2FjYSIsImh0dHBzOi8vc3d5ZnR4LmNvbS5hdS8tbWZhX2VuYWJsZWQiOnRydWUsImh0dHBzOi8vc3d5ZnR4LmNvbS5hdS8tY291bnRyeV9uYW1lIjoiQXVzdHJhbGlhIiwiaHR0cHM6Ly9zd3lmdHguY29tLmF1Ly1jaXR5X25hbWUiOiJTeWRuZXkiLCJpc3MiOiJodHRwczovL3N3eWZ0eC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBhMmZiYTE2MzAyYzYwMDY5M2ZmY2M5IiwiYXVkIjoiaHR0cHM6Ly9hcGkuc3d5ZnR4LmNvbS5hdS8iLCJpYXQiOjE2MzE1MzMyNjgsImV4cCI6MTYzMjEzODA2OCwiYXpwIjoiRVF3M2ZhQXhPVGhSWVRaeXkxdWxaRGk4REhSQVlkRU8iLCJzY29wZSI6ImFwcC5hY2NvdW50LnRheC1yZXBvcnQgYXBwLmFjY291bnQuYmFsYW5jZSBhcHAuYWNjb3VudC5yZWFkIGFwcC5hZGRyZXNzLnJlYWQgYXBwLmZ1bmRzLnJlYWQgYXBwLm9yZGVycyBhcHAub3JkZXJzLmNyZWF0ZSBhcHAub3JkZXJzLmRlbGV0ZSBhcHAub3JkZXJzLnJlYWQgYXBwLm9yZGVycy5kdXN0IG9mZmxpbmVfYWNjZXNzIiwiZ3R5IjoicGFzc3dvcmQifQ.OXp-VvsRkaf7VOpV5lPA1qGb2GZ28wXDFfg9mhGc7vQqwtfJ1sZI5OXDloJdKvXOWRY9OWFvRfe0rBaI0TQm0tAwkK6yCa4p4LY7FyoIsq_7GQ5hAIEyqr9PKDMXAh6Wyy2DUdoevFiM-ESZrsrpUhmL4s3urq8zvp2I_pjFKa1XTiDKtm81sniJ1YORNIFCkIjah8Ac2I-nCgrUihaV-KgXxhSrkurPswnxX5Nq41KTO4JkugUbRrGETHi3WG-kaeFgiBFFtbNyrHxt0_OSVBvMoaGxFFNS9MMNWUcMAxhofkr-veUbEHZpVhPUspeVrm55YoTJfZyia4-LGjsh_g'
        else:
            self.base_url = 'https://api.swyftx.com.au'

            def retrieve_jwt():
                # Generates a jwt that will be active for 1 week with the permissions associated with API Key
                response = requests.post(self.base_url + '/auth/refresh/', data=self.data)

                if response.status_code == 200:
                    return response.json()['accessToken']
                else:
                    logger.error("Error whilst making request for JWT: %s (error code %s)",
                                 response.json(), response.status_code)
                    return None

            self.token = retrieve_jwt()

        self.prices = dict()

        self.header = {'Content-Type':'application/json',
                       'Authorization': 'Bearer ' + self.token}

        logger.info("Swyftx Client successfully initialized")

    def make_request(self, method, endpoint, data, header):
        if method == "GET":
            response = requests.get(self.base_url + endpoint, params=data, headers=self.header)
        elif method == "POST":
            response = requests.post(self.base_url + endpoint, data=data, headers=self.header)
        elif method == "DELETE":
            response = requests.delete(self.base_url + endpoint, data=data, headers=self.header)
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error whilst making %s request to %s: %s (error code %s)",
                         method, endpoint, response.json(), response.status_code)
            return None

    # Data methods that call public endpoints
    def get_contracts(self):
        exchange_info = self.make_request("GET", "/markets/assets/", None, None)
        if exchange_info is not None:
            assets = []
            for asset in exchange_info:
                assets.append({'assetId': asset['id'], 'assetCode': asset['code']})
        return assets

    def get_historical_candles(self, symbol, resolution):
        data = dict()
        data['baseAsset'] = "AUD"
        data['secondaryAsset'] = symbol
        data['timeStart'] = 1000 * int(datetime.datetime.utcnow().timestamp()) - 3600000
        data['timeEnd'] = 1000 * int(datetime.datetime.utcnow().timestamp())
        data['resolution'] = resolution
        data['limit'] = 1000

        raw_candles = self.make_request("GET", "/charts/getBars/AUD/" + symbol + "/ask/", data, None)['candles']
        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                # pprint.pprint(c)
                candles.append([float(c['close']), float(c['high']), float(c['low']), float(c['open']),
                                c['time'], c['volume']])
        return candles

    def get_bid_ask(self, symbol):
        bid_ask_info = self.make_request("GET", "/markets/info/basic/"+symbol+"/",data=None, header=None)[0]
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

    def get_balance(self):
        """Returns the balances in an account for each asset
        Note: returns the assetId, not the asset Name"""
        balances = dict()
        response = self.make_request("GET", "/user/balance/", None, self.header)
        if response is not None:
            for a in response:
                balances[a['assetId']] = a
        pprint.pprint(balances)
        return balances

    def place_order(self, primary, secondary, quantity, assetQuantity, orderType, trigger):

        order_data = dict()
        order_data["primary"] = primary  # "USD"
        order_data["secondary"] = secondary  # "BTC"
        order_data["quantity"] = quantity  # "1000"
        order_data["assetQuantity"] = assetQuantity  # "USD"
        order_data["orderType"] = orderType  # 0
        order_data["trigger"] = trigger  # "52000"

        response = self.make_request("POST", "/orders/", data=json.dumps(order_data), header=self.header)
        # pprint.pprint(response.json())
        return response

    def cancel_order(self):
        return
    #
    # def get_order_status(self):
    #     return
