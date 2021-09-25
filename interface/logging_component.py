import tkinter as tk
from interface.styling import *

class Logging(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logging_text = tk.Text(self, height=10, width=60, state = tk.DISABLED, bg=BG_COLOUR, fg=FG_COLOUR_2,
                                    font=GLOBAL_FONT)
        self.logging_text.pack(side=tk.TOP)

    def add_log(self, message):
            self.logging_text.configure(state=tk.NORMAL)
            self.logging_text.insert("1.0", message + "\n")
            self.logging_text.configure(state=tk.DISABLED)