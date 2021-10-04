import tkinter as tk
import typing

from models import *

from interface.styling import *
from interface.autocomplete_widget import Autocomplete
from interface.scrollable_frame import ScrollableFrame


class Watchlist(tk.Frame):
    def __init__(self, swyftx_assets: typing.Dict[str, Asset],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.db = WorkspaceData()

        self.swyftx_symbols = list(swyftx_assets.keys())

        self._commands_frame = tk.Frame(self, bg=BG_COLOUR)
        self._commands_frame.pack(side=tk.TOP)

        colour = BG_COLOUR
        self._table_frame = tk.Frame(self, bg=colour)
        self._table_frame.pack(side=tk.TOP)

        self._swyftx_label = tk.Label(self._commands_frame, text="Swyftx", bg=colour, fg=FG_COLOUR, font=BOLD_FONT)
        self._swyftx_label.grid(row=0, column=0)

        self._swyftx_entry = Autocomplete(self.swyftx_symbols, self._commands_frame, fg=FG_COLOUR, justify=tk.CENTER,
                                          insertbackground=FG_COLOUR, bg=BG_COLOUR_2, highlightthickness=False)
        self._swyftx_entry.bind("<Return>", self._add_swyftx_symbol)
        self._swyftx_entry.grid(row=1, column=0, padx=5)

        self.body_widgets = dict()

        self._headers = ["symbol", "exchange", "bid", "ask", "remove"]

        self._headers_frame = tk.Frame(self._table_frame, bg=colour)

        self._col_width = 13

        # Creates the headers dynamically

        for idx, h in enumerate(self._headers):
            header = tk.Label(self._headers_frame, text=h.capitalize() if h != "remove" else "", bg=colour,
                              fg=FG_COLOUR, font=GLOBAL_FONT, width=self._col_width)
            header.grid(row=0, column=idx)

        header = tk.Label(self._headers_frame, text="", bg=colour,
                          fg=FG_COLOUR, font=GLOBAL_FONT, width=2)
        header.grid(row=0, column=len(self._headers))

        self._headers_frame.pack(side=tk.TOP, anchor="nw")

        # Creates the table body

        self._body_frame = ScrollableFrame(self._table_frame, bg=colour, height=250)
        self._body_frame.pack(side=tk.TOP, fill=tk.X, anchor="nw")

        # Add keys to the body_widgets dictionary, the keys represents columns or data related to a column
        # You could also have another logic: instead of body_widgets[column][row] have body_widgets[row][column]
        for h in self._headers:
            self.body_widgets[h] = dict()
            if h in ["bid", "ask"]:
                self.body_widgets[h + "_var"] = dict()

        self._body_index = 0

    def _remove_symbol(self, b_index: int):

        for h in self._headers:
            self.body_widgets[h][b_index].grid_forget()
            del self.body_widgets[h][b_index]

    def _add_swyftx_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.swyftx_symbols:
            self._add_symbol(symbol, "Swyftx")
            event.widget.delete(0, tk.END)

    def _add_symbol(self, symbol: str, exchange: str):

        b_index = self._body_index

        self.body_widgets['symbol'][b_index] = tk.Label(self._body_frame.sub_frame, text=symbol, bg=BG_COLOUR,
                                                        fg=FG_COLOUR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['symbol'][b_index].grid(row=b_index, column=0)

        self.body_widgets['exchange'][b_index] = tk.Label(self._body_frame.sub_frame, text=exchange, bg=BG_COLOUR,
                                                          fg=FG_COLOUR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['exchange'][b_index].grid(row=b_index, column=1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()
        self.body_widgets['bid'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['bid_var'][b_index],
                                                     bg=BG_COLOUR, fg=FG_COLOUR_2, font=GLOBAL_FONT,
                                                     width=self._col_width)
        self.body_widgets['bid'][b_index].grid(row=b_index, column=2)

        self.body_widgets['ask_var'][b_index] = tk.StringVar()
        self.body_widgets['ask'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['ask_var'][b_index],
                                                     bg=BG_COLOUR, fg=FG_COLOUR_2, font=GLOBAL_FONT,
                                                     width=self._col_width)
        self.body_widgets['ask'][b_index].grid(row=b_index, column=3)

        self.body_widgets['remove'][b_index] = tk.Button(self._body_frame.sub_frame, text="X",
                                                         bg="darkred", fg=FG_COLOUR, font=GLOBAL_FONT,
                                                         command=lambda: self._remove_symbol(b_index), width=4)
        self.body_widgets['remove'][b_index].grid(row=b_index, column=4)

        self._body_index += 1
