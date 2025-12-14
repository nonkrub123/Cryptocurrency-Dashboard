import tkinter as tk
from tkinter import ttk
import requests
import websocket
import threading
import json
import time
class CryptoOrderBook:
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False

        # Create UI inside Parent frame
        # Configure parent frame by grid
        parent.columnconfigure(0, weight = 1)
        parent.rowconfigure(0, weight = 1)

        # Configure frame layout by grid
        self.frame = tk.Frame(parent, bg="gray")
        self.frame.columnconfigure((0,1), weight=1, minsize=10)
        self.frame.rowconfigure(0, weight=2, minsize=10)
        self.frame.rowconfigure(1, weight=2, minsize=10)
        self.frame.rowconfigure(2, weight=20, minsize=10)

        # Create Bid Frame & Ask Frame
        self.bid_frame = tk.Frame(self.frame, bg="white")
        self.bid_frame.grid(row=2, column=0, sticky="nsew")

        self.ask_frame = tk.Frame(self.frame, bg="white")
        self.ask_frame.grid(row=2, column=1, sticky="nsew")

        # Allow them to stretch
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        # Create bid/ask data containers
        self.bid_list = []
        self.ask_list = []

        # Build Bid/Ask UI
        self.create_book_section(self.bid_frame, self.ask_frame, self.bid_list, self.ask_list)

        # The rest of the ui
        self.title_name = tk.Label(self.frame, text=display_name, bg="white", font=("arial", 16))
        self.title_name.grid(row=0, column=0,columnspan=2, sticky="nsew")

        self.bid_label = tk.Label(self.frame, 
                                  text="BID (Buys-Highest to lowest price)", bg="white", font=("arial", 10))
        self.bid_label.grid(row=1, column=0, sticky="nsew")

        self.ask_label = tk.Label(self.frame, 
                                  text="ASK (Sells-Highest to lowest price)", bg="white", font=("arial", 10))
        self.ask_label.grid(row=1, column=1, sticky="nsew")


    def init_book_txt(self, lists, parent):
        for i in range(10):
            lists.append({
                "price": tk.Label(parent, text=f"{i}", font=("arial",10)),
                "quantity": tk.Label(parent, text=f"{i}", font=("arial",10))
            })

    def create_book_section(self, bid_frame, ask_frame, bid_list, ask_list):

        for frame in (bid_frame, ask_frame):
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

        # ----- HEADERS -----
        tk.Label(bid_frame, text="Price", font=("arial", 10, "bold")).grid(
            row=0, column=0, sticky="nsew", padx=2
        )
        tk.Label(bid_frame, text="Quantity", font=("arial", 10, "bold")).grid(
            row=0, column=1, sticky="nsew", padx=2
        )

        tk.Label(ask_frame, text="Price", font=("arial", 10, "bold")).grid(
            row=0, column=0, sticky="nsew", padx=2
        )
        tk.Label(ask_frame, text="Quantity", font=("arial", 10, "bold")).grid(
            row=0, column=1, sticky="nsew", padx=2
        )

        # ----- DATA -----
        self.init_book_txt(bid_list, bid_frame)
        self.init_book_txt(ask_list, ask_frame)

        for i, row in enumerate(bid_list):
            row["price"].grid(row=i+1, column=0, sticky="nsew", padx=2)
            row["quantity"].grid(row=i+1, column=1, sticky="nsew", padx=2)

        for i, row in enumerate(ask_list):
            row["price"].grid(row=i+1, column=0, sticky="nsew", padx=2)
            row["quantity"].grid(row=i+1, column=1, sticky="nsew", padx=2)


    def start(self):
        if self.is_active == True:
            return
        
        self.is_active = True
        threading.Thread(target=self.update_display, daemon=True).start()

    def stop(self):
        self.is_active = False

    def update_display(self):
        while self.is_active:
            url = "https://api.binance.com/api/v3/depth"
            params = {"symbol": self.symbol.upper(), "limit": 10}
            data = requests.get(url, params=params).json()

            self.frame.after(0, self.apply_book_update, data)
            time.sleep(0.01)

    def apply_book_update(self, data):
        bids = data["bids"]
        asks = data["asks"]

        for i in range(min(10, len(bids))):
            price, quantity = bids[i]
            self.bid_list[i]["price"].config(text=price)
            self.bid_list[i]["quantity"].config(text=quantity)

        for i in range(min(10, len(asks))):
            price, quantity = asks[i]
            self.ask_list[i]["price"].config(text=price)
            self.ask_list[i]["quantity"].config(text=quantity)

    def show(self):
        self.frame.grid(column=0, row=0, sticky="nsew")
    def grid_forget(self):
        self.frame.grid_forget()