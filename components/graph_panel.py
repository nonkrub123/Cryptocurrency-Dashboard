import tkinter as tk
import threading
import requests
import time
from datetime import datetime
import numpy as np
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import tkinter as tk
import threading
import requests
import time
from datetime import datetime
import numpy as np
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CryptoGraph:
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.upper()
        self.display_name = display_name

        self.is_active = False

        # ===== FRAME =====
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self.frame = tk.Frame(parent, bg="white")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        # ===== FIGURE =====
        self.fig = Figure(figsize=(5, 4), dpi=100, facecolor="white")
        self.ax_price = self.fig.add_subplot(211)
        self.ax_vol = self.fig.add_subplot(212, sharex=self.ax_price)

        self.style_axes()
        self.fig.autofmt_xdate()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # ---------- STYLE ----------
    def style_axes(self):
        for ax in (self.ax_price, self.ax_vol):
            ax.set_facecolor("#f7f7f7")
            ax.grid(True, color="#cccccc", linestyle="--", linewidth=0.4)
            ax.tick_params(colors="#333333")

        self.ax_price.set_ylabel("Price", color="#333333", fontsize=9)
        self.ax_vol.set_ylabel("Volume", color="#333333", fontsize=9)

    # ---------- DATA ----------
    def fetch_klines(self):
        try:
            url = "https://api.binance.com/api/v3/klines"
            params = {
                "symbol": self.symbol,
                "interval": "1h",
                "limit": 50
            }
            data = requests.get(url, params=params, timeout=5).json()
            return data if isinstance(data, list) else []
        except Exception:
            return []

    # ---------- DRAW ----------
    def draw(self, klines):
        if not klines:
            return

        self.ax_price.clear()
        self.ax_vol.clear()
        self.style_axes()

        times = [datetime.fromtimestamp(k[0] / 1000) for k in klines]
        ohlc = np.array([[float(x) for x in k[1:5]] for k in klines])
        volumes = np.array([float(k[5]) for k in klines])

        width = 0.6

        # Candles
        for i, (o, h, l, c) in enumerate(ohlc):
            color = "#2ecc71" if c >= o else "#e74c3c"
            self.ax_price.plot([i, i], [l, h], color=color, linewidth=1)
            self.ax_price.add_patch(
                patches.Rectangle(
                    (i - width / 2, min(o, c)),
                    width,
                    max(abs(c - o), 0.0001),
                    facecolor=color,
                    edgecolor=color
                )
            )

        # Volume
        for i, v in enumerate(volumes):
            color = "#2ecc71" if ohlc[i][3] >= ohlc[i][0] else "#e74c3c"
            self.ax_vol.bar(i, v, color=color, width=width)

        # --- clean time axis ---
        step = max(1, len(times) // 5)
        ticks = list(range(0, len(times), step))

        self.ax_vol.set_xticks(ticks)
        self.ax_vol.set_xticklabels(
            [times[i].strftime("%m-%d %H:%M") for i in ticks],
            fontsize=8,
            color="#333333",
            rotation=30,
            ha="right"
        )

        self.ax_price.tick_params(labelbottom=False)

        self.ax_price.set_title(
            f"{self.display_name} | 1H Candles",
            color="#222222",
            fontsize=10
        )

        self.fig.tight_layout()
        self.canvas.draw_idle()

    # ---------- LOOP ----------
    def update_loop(self):
        while self.is_active:
            data = self.fetch_klines()
            if data:
                self.frame.after(0, self.draw, data)
            time.sleep(3)

    # ---------- CONTROL ----------
    def start(self):
        if self.is_active:
            return

        self.is_active = True
        threading.Thread(
            target=self.update_loop,
            daemon=True
        ).start()

    def stop(self):
        self.is_active = False

    # ---------- VISIBILITY ----------
    def show(self):
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.start()

    def grid_forget(self):
        self.stop()
        self.frame.grid_forget()
