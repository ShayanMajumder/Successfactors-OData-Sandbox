# main.py
from gui.app import App
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)  # Disable resizing
    app = App(root)
    root.mainloop()
