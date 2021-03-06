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

    # Instantiate a TK object (application)
    root = tk.Tk()

    # A loop is required to prevent the program from terminating
    root.mainloop()
