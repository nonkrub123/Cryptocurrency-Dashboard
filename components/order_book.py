import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
class CryptoOrderBook:
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None

        # Create UI inside Parent frame
        # We use grid to handle this
        self.frame = tk.Frame(parent, bg="gray")
        self.frame.columnconfigure((0,1), weight=1, minsize=10)
        self.frame.rowconfigure(0, weight=2, minsize=10)
        self.frame.rowconfigure(1, weight=2, minsize=10)
        self.frame.rowconfigure(2, weight=10, minsize=10)

        self.title_name = tk.Label(self.frame, text=display_name, bg="white")
        self.title_name.grid(row=0, column=0,columnspan=2)

        self.bid_label = tk.Label(self.frame, text="BID (Buys-Highest to lowest price)", bg="white")
        self.bid_label.grid(row=1, column=0)

        self.ask_label = tk.Label(self.frame, text="ASK (Sells-Highest to lowest price)", bg="white")
        self.ask_label.grid(row=1, column=1)

        self.frame.grid(column=0, row=0)
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def on_message(self):
        pass
    def update_display(self):
        pass
    def show(self):
        pass
    def grid_forget(self):
        pass