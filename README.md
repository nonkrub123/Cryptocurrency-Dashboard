# Crypto Currency Board

Crypto Currency Board is a desktop application built with Python and Tkinter that displays real-time cryptocurrency market data using Binance APIs.

The application allows users to switch between multiple cryptocurrencies and view live price updates, best bid/ask prices, spread calculations, and order book snapshots.

The system is designed using modular, object-oriented components and handles real-time data streaming with background threads while keeping the UI responsive and thread-safe.

⚠️ **Note:** The order book snapshot is not fully real-time (it uses REST API polling), but it updates frequently and stays very close to live data.

---

## Overview

Crypto Currency Board demonstrates:

- Real-time data streaming
- Event-driven programming
- Thread-safe GUI updates
- Modular object-oriented design
- Responsive Tkinter layouts

---

## Project Structure


## Project Structure
```
turtle_graphics/
│
├── README.md                          # This file
│
├── Final_ui_design.png
│
├── presentation.mp4
│
├── requirements.txt
│
├── main.py
│
├── Component/
│   ├──__init__.py
│   ├── cryptoboardapp.py
│   ├── order_book.py
│   ├── technical.py
│   ├── ticker_class.py
```


---

## Features

### ✅ Real-Time Market Data

- Live cryptocurrency price updates via Binance WebSocket API
- Automatic price change and percentage calculation
- No manual refresh required

---

### ✅ Multi-Coin Support

- Supports multiple trading pairs:
  - BTC
  - ETH
  - SOL
  - BNB
  - XRP
- One-click coin selection using buttons
- Automatically switches displayed data when a new coin is selected

---

### ✅ Best Bid / Ask & Spread Analysis

- Displays the current highest bid (buy price)
- Displays the current lowest ask (sell price)
- Calculates and shows bid–ask spread in real time
- Updates instantly from live market data

---

### ✅ Order Book Snapshot

- Displays top bid and ask levels from the order book
- Clearly separates buy and sell sides
- Updates frequently using REST API polling

⚠️ Uses REST API, so there may be a small delay compared to WebSocket streams.

---

## Architecture Overview

### ✅ WebSocket-Based Data Streaming

- Uses Binance WebSocket streams for low-latency market data
- Avoids repeated REST API calls for ticker data
- Efficient and responsive real-time updates

---

### ✅ Thread-Safe UI Updates

- WebSocket connections run in background threads
- Tkinter UI updates are handled using `tk.after`
- Prevents UI freezing and race conditions

---

### ✅ Modular & Reusable Design

The application is divided into reusable components:

- Ticker display
- Technical analysis panel
- Order book display

Each component is independent and easy to extend with new features or indicators.

---

### ✅ Responsive Layout

- UI adapts to window resizing
- Grid-based layout with weighted rows and columns
- Clear separation between ticker, analysis, and order book sections

---

## Module Responsibilities

### 1. CryptoBoardApp

**Responsibility:**  
Acts as the main application controller and layout manager.

**Details:**
- Initializes the main window and overall UI layout
- Manages top, middle, and bottom frames
- Handles coin selection and view switching
- Coordinates interaction between ticker, technical analysis, and order book modules
- Manages application lifecycle (start, stop, close)

---

### 2. CryptoTicker

**Responsibility:**  
Handles real-time price data for a selected cryptocurrency.

**Details:**
- Connects to Binance WebSocket ticker stream
- Receives live price, price change, and percentage change
- Updates price display in real time
- Sends relevant market data to the technical analysis module
- Starts and stops WebSocket connections as needed

---

### 3. TechnicalAnalysis

**Responsibility:**  
Displays derived market metrics based on live ticker data.

**Details:**
- Receives best bid and best ask prices
- Calculates and displays bid–ask spread
- Updates UI safely using Tkinter’s event loop
- Provides simplified market insight for the user

---

### 4. CryptoOrderBook

**Responsibility:**  
Displays a snapshot of the market depth.

**Details:**
- Retrieves order book data (top bid and ask levels)
- Displays buy and sell orders in a structured layout
- Updates data periodically using REST API
- Manages start/stop behavior to reduce unnecessary data usage

---

## How to Run

### Requirements

- Python 3.11+
- Internet connection

### Install Dependencies

```bash
pip install websocket-client requests numpy
```

### Run the Application
```bash
python main.py