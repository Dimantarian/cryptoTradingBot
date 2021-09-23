# This file is for testing functionality before adding to main.py

import pprint
import tkinter as tk
import logging
from connectors.swyftx import SwyftxClient
from connectors.btcmarkets import BTCMarketsClient
from creds.creds import creds

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':
    # # Get data
    swyftx = SwyftxClient(False, creds['prodPublicKey'])
    #
    # # Test private endpoint
    pprint.pprint(swyftx.get_balance())
    # pprint.pprint(swyftx.get_assets())
    #
    # # swyftx.place_order("USD", "SOL", "100", "USD", 3, 200)
    #
    # # Test pulling back the first/last order
    # oldest_order = swyftx.get_all_orders("SOL")['orders'][0]['orderUuid']
    # pprint.pprint(swyftx.get_order_status(oldest_order))
    # most_recent_order = swyftx.get_all_orders("SOL")['orders'][-1]['orderUuid']
    # pprint.pprint(swyftx.get_order_status(most_recent_order))
    #
    # # Test cancelling an order
    # swyftx.place_order("USD", "SOL", "2000", "USD", 3, 25)
    # most_recent_order = swyftx.get_all_orders("SOL")['orders'][-1]['orderUuid']
    # swyftx.cancel_order(most_recent_order)

    # Test BTCMarkets Websocket
    # btc = BTCMarketsClient(creds['btcPublicKey'],
    #                        creds['btcPrivateKey'])

    # Instantiate a TK object (application)
    # root = tk.Tk()

    # A loop is required to prevent the program from terminating
    # root.mainloop()
