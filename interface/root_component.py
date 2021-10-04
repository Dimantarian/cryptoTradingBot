import tkinter as tk
from interface.styling import *
from interface.logging_component import *
from connectors.swyftx import SwyftxClient
from connectors.btcmarkets import BTCMarketsClient
from interface.watchlist_component import Watchlist


class Root(tk.Tk):
    def __init__(self, swyftx: SwyftxClient, btc: BTCMarketsClient):
        super().__init__()

        self.swyftx = swyftx
        self.btc = btc

        self.title("Trading Bot")

        self.configure(bg=BG_COLOUR)

        self._left_frame = tk.Frame(self, bg=BG_COLOUR)
        self._left_frame.pack(side=tk.LEFT)

        self._right_frame = tk.Frame(self, bg=BG_COLOUR)
        self._right_frame.pack(side=tk.LEFT)

        # Creates and places components at the top and bottom of the left and right frame

        self._watchlist_frame = Watchlist(self.swyftx.assets, self._left_frame, bg=BG_COLOUR)
        self._watchlist_frame.pack(side=tk.TOP, padx=10)

        self._logging_frame = Logging(self._left_frame, bg=BG_COLOUR)
        self._logging_frame.pack(side=tk.TOP)

        self._update_ui()

    def _update_ui(self):
        for log in self.swyftx.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        for log in self.btc.logs:
            if not log['displayed']:
                self._logging_frame.add_log(log['log'])
                log['displayed'] = True

        self.after(1500, self._update_ui)
