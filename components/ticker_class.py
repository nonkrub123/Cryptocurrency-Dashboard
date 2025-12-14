import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
from components.technical import TechinalAnalysis
class CryptoTicker:
    """Reusable ticker component for any cryptocurrency."""
    
    def __init__(self, parent, symbol, display_name, technical_analysis=None):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.ws = None
        self.technical_analysis = technical_analysis

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
        
        highest = float(data['b'])
        lowest = float(data['a'])
        spread = highest - lowest

        # Call callback if provided
        if self.technical_analysis:
            try:
                self.technical_analysis.on_data(highest, lowest, spread)
            except Exception as e:
                print(f"Callback error: {e}")

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