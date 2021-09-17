# This file is for testing functionality before adding to main.py

import pprint
import tkinter as tk
import logging
from connectors.swyftx import SwyftxClient
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
    # Get data
    swyftx = SwyftxClient(False, creds['demoPublicKey'])
    pprint.pprint(swyftx.get_balance())
    # pprint.pprint(swyftx.place_order("USD", "SOL", "5000", "USD", 1, None))
    pprint.pprint(swyftx.get_historical_candles("BTC", "1h", None, None))
    pprint.pprint(swyftx.get_bid_ask("BTC"))

    # pprint.pprint(swyftx.get_assets())

    # Instantiate a TK object (application)
    root = tk.Tk()

    # A loop is required to prevent the program from terminating
    root.mainloop()
