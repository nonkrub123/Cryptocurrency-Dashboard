import tkinter as tk
from tkinter import ttk
import websocket
import threading
import json
class TechinalAnalysis:
    def __init__(self, parent, display_name):
        self.parent = parent
        # self.symbol = symbol.lower()
        self.display_name = display_name
        self.is_active = False
        self.is_show = True
        self.init_ui()

    def init_ui(self):
        # make parent stretchable
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        container = tk.Frame(self.parent, bg="white")
        container.grid(row=0, column=0, sticky="nsew")

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)

        self.frame = tk.Frame(container, bg="white")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # grid layout inside frame
        self.frame.columnconfigure(0, weight=8, minsize=30, uniform="ta")
        self.frame.columnconfigure(1, weight=6, minsize=30, uniform="ta")
        self.frame.rowconfigure((0,1,2,3), weight=1, minsize=30, uniform="ta")

        self.title = tk.Label(self.frame, text=self.display_name,
                            font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, columnspan=4)

        self.label = tk.Label(self.frame, text="Bid (buy)",
                            font=("Arial", 13, "bold"))
        self.label.grid(row=1, column=0)

        self.highest_label = tk.Label(self.frame, text="-",
                            font=("Arial", 11, "bold"))
        self.highest_label.grid(row=1, column=1)

        self.label2 = tk.Label(self.frame, text="Ask (sell)",
                            font=("Arial", 13, "bold"))
        self.label2.grid(row=2, column=0)

        self.lowest_label = tk.Label(self.frame, text="-",
                            font=("Arial", 11, "bold"))
        self.lowest_label.grid(row=2, column=1)

        self.label3 = tk.Label(self.frame, text="Spread",
                            font=("Arial", 13, "bold"))
        self.label3.grid(row=3, column=0)

        self.spread_label = tk.Label(self.frame, text="-",
                            font=("Arial", 11, "bold"))
        self.spread_label.grid(row=3, column=1)
    
    def on_data(self, highest, lowest, spread):
        # always jump to UI thread
        self.frame.after(
            0,
            self._update_ui,
            highest, lowest, spread
        )

    def _update_ui(self, highest, lowest, spread):
        self.highest_label.config(text=f"{highest:.2f}")
        self.lowest_label.config(text=f"{lowest:.2f}")

        if spread <= 0:
            color = "#FF5349"
        else:
            color = "green"
        self.spread_label.config(text=f"{abs(spread):.2f}",fg=color)

    def show(self):
        self.frame.grid(row=0, column=0, sticky="nsew")

    def grid_forget(self):
        self.frame.grid_forget()