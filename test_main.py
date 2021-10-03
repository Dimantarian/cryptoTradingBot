# This file is for testing functionality before adding to main.py

import pprint
import tkinter as tk
import time
import logging
from connectors.swyftx import SwyftxClient
from connectors.btcmarkets import BTCMarketsClient
from creds.creds import creds
from interface.root_component import *

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
    swyftx = SwyftxClient(False, creds['prodPublicKey'])
    btc = BTCMarketsClient(creds['btcPublicKey'],
                           creds['btcPrivateKey'])

    # Instantiate a TK object (application)
    root = Root(swyftx, btc)
    # A loop is required to prevent the program from terminating
    root.mainloop()
