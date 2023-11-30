from tkinter import *
from tkinter import ttk

 ""
class Load:
    def __init__(self):
        root = Tk()
        root.title("loading")
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry(f"{x}x{y}+0+0")
        root.attributes('-fullscreen', True)
        root.configure(background="#1c1c1c")
        bar = ttk.Progressbar(orient="horizontal")
        bar.pack(fill=X, padx=100, pady=y/3)
        bar.start()
        root.mainloop()
