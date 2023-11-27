from tkinter import *
from tkinter import ttk
from os import getpid
import json

class Load:
    def __init__(self):

        data = self.json_read()
        data['load_pid'] = getpid()
        self.json_write(data)

        self.root = Tk()
        self.root.title("loading")

    def main(self):
        x = self.root.winfo_screenwidth()
        y = self.root.winfo_screenheight()
        self.root.geometry(f"{x}x{y}+0+0")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="#1c1c1c")
        bar = ttk.Progressbar(orient="horizontal")
        bar.pack(fill=X, padx=100, pady=y/3)
        bar.start()
        self.root.mainloop()

    def json_read(self):
        with open("variables.json", "r", encoding="utf-8") as f:
            all_variables = json.load(f)
            return all_variables

    def json_write(self, data):
        with open("variables.json", "w", encoding="utf-8") as f:
            json.dump(data, f)