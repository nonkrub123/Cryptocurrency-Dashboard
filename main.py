import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
# =========================
#  REUSABLE TICKER CLASS
# =========================
class CryptoTicker:
    """Reusable ticker component for any cryptocurrency."""
    
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None
        
        # Create UI inside given parent frame (middle_frame)
        self.frame = ttk.Frame(parent, relief="solid", borderwidth=1, padding=20)
        
        ttk.Label(self.frame, text=display_name, font=("Arial", 14, "bold")).pack()
        
        self.price_label = tk.Label(self.frame, text="--,---", 
                                    font=("Arial", 20, "bold"), )
        self.price_label.pack(pady=2.5)
        
        self.change_label = ttk.Label(self.frame, text="--", 
                                      font=("Arial", 10))
        self.change_label.pack()
    
    def start(self):
        if self.is_active:
            return
        
        self.is_active = True
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"
        
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{self.symbol} error: {err}"),
            on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
            on_open=lambda ws: print(f"{self.symbol} connected")
        )
        
        threading.Thread(target=self.ws.run_forever, daemon=True).start()
    
    def stop(self):
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None
    
    def on_message(self, ws, message):
        if not self.is_active:
            return
        
        data = json.loads(message)
        price = float(data['c'])
        change = float(data['p'])
        percent = float(data['P'])
        
        self.parent.after(0, self.update_display, price, change, percent)
    
    def update_display(self, price, change, percent):
        if not self.is_active:
            return
        
        color = "green" if change >= 0 else "red"
        self.price_label.config(text=f"{price:,.2f}", fg=color)
        
        sign = "+" if change >= 0 else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            foreground=color
        )
    
    def show(self, row=0, column=0):
        self.frame.grid(row=row, column=column, sticky="nswe")
    
    def grid_forget(self):
        self.frame.grid_forget()

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

        # Widgets
        button1 = ttk.Button(self.top_frame, text = 'BTC', command=lambda: self.show_ticker("BTC"))
        button2 = ttk.Button(self.top_frame, text = 'ETH', command=lambda: self.show_ticker("ETH"))
        button3 = ttk.Button(self.top_frame, text = 'SOL', command=lambda: self.show_ticker("SOL"))
        button4 = ttk.Button(self.top_frame, text = 'BNB', command=lambda: self.show_ticker("BNB"))
        button5 = ttk.Button(self.top_frame, text = 'XRP', command=lambda: self.show_ticker("XRP"))

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
        self.tickers_frame.columnconfigure(0, weight=1)
        self.tickers_frame.rowconfigure(0, weight=1)
        self.tickers_frame.grid(row=0, column=0, sticky="nsew", padx=3)

        # Create tickers
        self.tickers = {
            "BTC": CryptoTicker(self.tickers_frame, "btcusdt", "BTC/UDST"),
            "ETH": CryptoTicker(self.tickers_frame, "ethusdt", "ETH/UDST"),
            "SOL": CryptoTicker(self.tickers_frame, "solusdt", "SOL/UDST"),
            "BNB": CryptoTicker(self.tickers_frame, "bnbusdt", "BNB/UDST"),
            "XRP": CryptoTicker(self.tickers_frame, "xrpusdt", "XRP/UDST")
        }

        # Show BTC as default display
        self.current = None
        self.show_ticker("BTC")

        root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def show_ticker(self, name):
        """Hide all tickers, show only selected one"""
        if self.current == name:
            return
        
        # Hidden and stop all
        for t in self.tickers.values():
            t.stop()
            t.grid_forget()
        
        # Show selected
        self.tickers[name].show()
        self.tickers[name].start()

        self.current = name
    
    def on_close(self):
        for t in self.tickers.values():
            t.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoBoardApp(root)
    root.mainloop()
