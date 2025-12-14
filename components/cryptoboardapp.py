import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
from components.ticker_class import CryptoTicker
from components.order_book import CryptoOrderBook
# =========================
#  REUSABLE TICKER CLASS
# =========================

class CryptoBoardApp:
    def __init__(self, root):
        # Create main window
        self.root = root
        self.root.title("Crypto Currency Board")
        self.root.geometry("900x600")

        # === ROOT GRID CONFIG ===
        self.root.columnconfigure(0, weight=1, uniform = "frame", min=20)
        self.root.rowconfigure(0, weight=1, uniform = "frame", min=30)
        self.root.rowconfigure(1, weight=5, uniform = "frame", min= 120)
        self.root.rowconfigure(2, weight=15, uniform = "frame")

        # === FRAMES ===
        self.top_frame = tk.Frame(root, bg='red', borderwidth=2, relief="solid", width=1, height=1)    # Top
        self.middle_frame = tk.Frame(root, bg='blue', borderwidth=2, relief="solid")   # middle
        self.bottom_frame = tk.Frame(root, bg='yellow', borderwidth=2, relief="solid") # Bottom

        self.top_frame.grid(row=0, column=0, sticky='NSEW', padx=5, pady=2)
        self.middle_frame.grid(row=1, column=0, sticky='NSEW', padx=5, pady=2)
        self.bottom_frame.grid(row=2, column=0, sticky='NSEW', padx=5, pady=2)

        # TOP BUTTONS
        self.top_frame.columnconfigure((0,1,2,3,4), weight=1, uniform="ua", minsize= 50)
        self.top_frame.columnconfigure(5, weight=10, uniform="ua")
        self.top_frame.rowconfigure(0, weight= 1,uniform="ua", minsize=30)

        # Widgetss
        button1 = ttk.Button(self.top_frame, text = 'BTC', command=lambda: self.show_selected("BTC"))
        button2 = ttk.Button(self.top_frame, text = 'ETH', command=lambda: self.show_selected("ETH"))
        button3 = ttk.Button(self.top_frame, text = 'SOL', command=lambda: self.show_selected("SOL"))
        button4 = ttk.Button(self.top_frame, text = 'BNB', command=lambda: self.show_selected("BNB"))
        button5 = ttk.Button(self.top_frame, text = 'XRP', command=lambda: self.show_selected("XRP"))

        # upper frame widget
        button1.grid(row=0, column= 0, sticky="nsew")
        button2.grid(row=0, column= 1, sticky="nsew")
        button3.grid(row=0, column= 2, sticky="nsew")
        button4.grid(row=0, column= 3, sticky="nsew")
        button5.grid(row=0, column= 4, sticky="nsew")

        # Middle FRAME
        self.middle_frame.columnconfigure(0, weight=3, uniform="mid", minsize=167)
        self.middle_frame.columnconfigure(1, weight=4, uniform="mid", minsize=30)
        self.middle_frame.columnconfigure(2, weight=4, uniform="mid", minsize=30)
        self.middle_frame.columnconfigure(3, weight=4, uniform="mid", minsize=30)
        self.middle_frame.rowconfigure(0, weight=1)
        
        # TICKER FRAME
        self.tickers_frame = tk.Frame(self.middle_frame, bg="white",)
        self.tickers_frame.grid(row=0, column=0, sticky="nsew", padx=3)
        self.tickers_frame.columnconfigure(0, weight=1)
        self.tickers_frame.rowconfigure(0, weight=1)

        # Create tickers
        self.tickers = {
            "BTC": CryptoTicker(self.tickers_frame, "btcusdt", "BTC/UDST"),
            "ETH": CryptoTicker(self.tickers_frame, "ethusdt", "ETH/UDST"),
            "SOL": CryptoTicker(self.tickers_frame, "solusdt", "SOL/UDST"),
            "BNB": CryptoTicker(self.tickers_frame, "bnbusdt", "BNB/UDST"),
            "XRP": CryptoTicker(self.tickers_frame, "xrpusdt", "XRP/UDST")
        }

        # Bottom Frame
        self.bottom_frame.columnconfigure(0, weight=9, minsize=100, uniform="bt")
        self.bottom_frame.columnconfigure(1, weight=10, minsize=100, uniform="bt")
        self.bottom_frame.rowconfigure(0, weight=1, uniform="bt")

        # ORDER BOOK FRAME
        self.order_book_frame = tk.Frame(self.bottom_frame, bg="blue")
        self.order_book_frame.grid(row=0,column=0,sticky="nsew", padx=3)

        # Create Order book
        self.order_book = {
            "BTC": CryptoOrderBook(self.order_book_frame, "btcusdt", "Order Book Snapshot"),
            "ETH": CryptoOrderBook(self.order_book_frame, "ethusdt", "Order Book Snapshot"),
            "SOL": CryptoOrderBook(self.order_book_frame, "solusdt", "Order Book Snapshot"),
            "BNB": CryptoOrderBook(self.order_book_frame, "bnbusdt", "Order Book Snapshot"),
            "XRP": CryptoOrderBook(self.order_book_frame, "xrpusdt", "Order Book Snapshot")
        }

        # Show BTC as default display
        self.current = None
        self.show_ticker("BTC")
        self.show_book("BTC")

        root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def show_selected(self,name):
        """Hide all ui, show only selected one"""
        if self.current == name:
            return
        
        self.show_ticker(name)
        self.show_book(name)

        self.current = name

    def show_ticker(self, name):
        """Hide all tickers, show only selected one"""
        # Hidden and stop all
        for t in self.tickers.values():
            t.stop()
            t.grid_forget()
        
        # Show selected
        self.tickers[name].show()
        self.tickers[name].start()
    
    def show_book(self, name):
        if self.current == name:
            return
        
        # Hidden and stop all
        for b in self.order_book.values():
            b.stop()
            b.grid_forget()

        self.order_book[name].show()
        self.order_book[name].start()

    def on_close(self):
        for t in self.tickers.values():
            t.stop()
        self.root.destroy()
