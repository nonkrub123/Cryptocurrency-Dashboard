import tkinter as tk
# from tkinter import ttk
from components.cryptoboardapp import CryptoBoardApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoBoardApp(root)
    root.mainloop()
