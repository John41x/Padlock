# utils.py
import tkinter as tk
import threading

def copy_to_clipboard(text: str):
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def clear_clipboard_after(seconds: int):
    def _clear():
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.destroy()
    threading.Timer(seconds, _clear).start()
