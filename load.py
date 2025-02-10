from tkinter import Tk
from tkinter import ttk
from os import system


class Load:
    def __init__(self):
        root = Tk()
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("Fancy.TButton", background="#1c1c1c", borderradius=5, foreground="white",
                        relief='ridge', width=12, font="Arial", anchor='center', padding=20)
        root.title("loading")
        root.iconbitmap(default='adm.ico')
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        root.geometry(f"{x}x{y}+0+0")
        root.attributes('-fullscreen', True)
        root.configure(background="#1c1c1c")
        bar = ttk.Progressbar(orient="horizontal")
        bar.pack(fill="x", padx=100, pady=y/3)
        bar.start()
        label = ttk.Label(root, text="Загрузка...", font=("Arial", 18, "bold"), background="#1c1c1c",
                               foreground="white")
        label.pack(pady=20)
        button = ttk.Button(root, command=self.reboot, text="Перезагрузить", style="Fancy.TButton")
        button.pack(pady=20)
        root.mainloop()

    def reboot(self):
        system("shutdown /r /t 1")