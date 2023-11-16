import time
import TKinterModernThemes as tkm
import qrcode
import tkinter
from tkinter import *
from tkinter import ttk
from TKinterModernThemes.WidgetFrame import nt
import json
import datetime
from prettytable import PrettyTable
from PIL import ImageTk, Image
import win32ui
import win32print
import win32ui
from PIL import Image, ImageWin
from variables import *

HORZRES = 8
VERTRES = 10

LOGPIXELSX = 88
LOGPIXELSY = 90

PHYSICALWIDTH = 110
PHYSICALHEIGHT = 110

PHYSICALOFFSETX = 5
PHYSICALOFFSETY = 5


class App(tkm.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("ADM_show", "Sun-valley", "dark", useconfigfile=False)
        self.client = ""
        self.account = ""
        self.int_receipt_number = 1
        self.receipt_number = f"Чек № {self.int_receipt_number}"
        self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
        self.day_status = day_state
        self.printer_name = win32print.GetDefaultPrinter() # "KPOS_58 Printer"
        self.edit_var = tkinter.StringVar()
        self.adres = "АДМ №213445 121096 г.Москва\nул.Кастанаевская, д.24 \nEMAIL: sales@deep2000.ru\n"
        self.label = None
        self.screen_pad = self.root.winfo_screenwidth() * 0.05

        # Global styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Arial", int(self.screen_pad*0.9), "bold"), justify='center')
        self.style.configure('x.TButton', font=("Arial", int(self.screen_pad*0.5), "bold"), foreground="red")
        self.style.configure('Treeview', font=("Arial", int(self.screen_pad*0.55)), rowheight=75, foreground="white", selectbackground='blue')
        self.style.configure('Treeview.Heading', font=("Arial", 40))
        self.style.map('Treeview', background=[('selected', '#57c8ff')], foreground=[('selected', 'black')])
        self.style.configure('TEntry', font=("Arial", int(self.screen_pad * 0.3)), foreground="white")
        self.style.layout('TNotebook.Tab', [])  # disable tabs layout

        # Notes
        self.notebook = self.Notebook("Notebook Test")
        self.tab1 = self.notebook.addTab("Авторизация")
        self.tab2 = self.notebook.addTab("Инкассация")
        self.tab3 = self.notebook.addTab("Внесение")
        self.tab4 = self.notebook.addTab("Выбор счета")
        self.tab5 = self.notebook.addTab("Чек")
        self.tab6 = self.notebook.addTab("Закр. опер. день")
        self.tab7 = self.notebook.addTab("Откр. опер. день")
        self.tab8 = self.notebook.addTab("Ошибка опер. день")

        # Tab1
        self.frame1 = self.tab1.addFrame("-")

        self.userinputvar = tkinter.StringVar(value="ЛОГИН")
        self.passinputvar = tkinter.StringVar(value="ПАРОЛЬ")

        self.user_field = self.frame1.Entry(textvariable=self.userinputvar, col=0, row=0, colspan=3)
        self.user_field.bind("<1>", lambda event: self.clear_user_entry())
        self.password_field = self.frame1.Entry(textvariable=self.passinputvar, col=0, row=1, colspan=3)
        self.password_field.bind("<1>", lambda event: self.clear_password_entry())
        self.user_field.configure(font=("Arial", int(self.screen_pad * 0.7), "bold"))
        self.password_field.configure(font=("Arial", int(self.screen_pad * 0.7), "bold"))

        self.button1 = self.frame1.Button("1", lambda: self.digit_buttons(self.button1), col=0, row=2)
        self.button2 = self.frame1.Button("2", lambda: self.digit_buttons(self.button2), col=1, row=2)
        self.button3 = self.frame1.Button("3", lambda: self.digit_buttons(self.button3), col=2, row=2)
        self.button4 = self.frame1.Button("4", lambda: self.digit_buttons(self.button4), col=0, row=3)
        self.button5 = self.frame1.Button("5", lambda: self.digit_buttons(self.button5), col=1, row=3)
        self.button6 = self.frame1.Button("6", lambda: self.digit_buttons(self.button6), col=2, row=3)
        self.button7 = self.frame1.Button("7", lambda: self.digit_buttons(self.button7), col=0, row=4)
        self.button8 = self.frame1.Button("8", lambda: self.digit_buttons(self.button8), col=1, row=4)
        self.button9 = self.frame1.Button("9", lambda: self.digit_buttons(self.button9), col=2, row=4)
        self.button0 = self.frame1.Button("   0   ", lambda: self.digit_buttons(self.button0), col=1, row=5)

        self.frame1.AccentButton("УДАЛ", self.backspace, col=0, row=5)
        self.frame1.AccentButton("ВВОД", self.authorization, col=2, row=5)

        # Tab2
        frame2 = self.tab2.addFrame("Инкассация")
        frame2.AccentButton("Открытие\nоперационного дня", self.day_open,
                            col=0, row=0, colspan=4, padx=self.screen_pad/2, pady=self.screen_pad/2)
        frame2.Button("Закрытие\nоперационного дня", self.day_close,
                      col=0, row=1, colspan=4, padx=self.screen_pad/2, pady=self.screen_pad/2)
        frame2.Button('❮', lambda: nt[0].select(0), col=4, rowspan=2,  style='x.TButton')

        # Tab3
        frame3 = self.tab3.addFrame("Внесение")
        deposit_frame = frame3.addLabelFrame("", col=0, row=1, colspan=5)
        button_frame = frame3.addFrame(name="", col=5, row=1)

        label_deposit = deposit_frame.Label(text="99999999")
        label_deposit.configure(font=("Arial", int(self.screen_pad), "bold"), width=9)
        label_down = frame3.Label("Внесите банкноты.\nМаксимальное колличество:\n200 банкнот", col=0, row=0, colspan=6)
        label_down.configure(font=("Arial", int(self.screen_pad*0.8)), foreground="#57c8ff", justify="center")
        self.done = button_frame.Button('Зачислить', self.receipt)
        frame3.Button('❮', lambda: nt[0].select(3), col=6, rowspan=2, style='x.TButton')

        # Tab4
        self.frame4 = self.tab4.addFrame("Выбор счета")
        label_up = self.frame4.Label("Выберете счет для зачисления", col=0, row=0, colspan=7)
        label_up.configure(font=("Arial", int(self.screen_pad * 0.8)), foreground="#57c8ff")
        with open('treeviewdata.json', encoding="utf-8") as f:
            tree = json.load(f)
        self.tree_data = self.frame4.Treeview(['Контрагент', 'Счет'], [110, 140], 3, tree,
                                              'subfiles', ['name', 'purpose'], col=0, row=1, colspan=7, rowspan=7)
        self.tree_data.selection_add(1)
        self.tree_data.configure(style="Treeview")
        self.tree_data.bind("<<TreeviewSelect>>", self.tree_selection)
        self.frame4.Button('❮', lambda: nt[0].select(0), col=7, rowspan=9, style='x.TButton')
        self.frame4.Button(text="Выбрать", col=0, row=8, colspan=7, command=lambda: nt[0].select(2))

        # Tab5
        self.frame5 = self.tab5.addFrame("Заберите чек")
        self.frame5.Label(text="", col=0, padx=self.screen_pad)
        self.frame5.Label(text="", row=0, col=1)

        self.qr_label = ttk.Label(self.frame5.master)
        self.qr_label.grid(row=4, column=1, columnspan=4, sticky=N)
        self.label5 = self.frame5.Label("Заберите чек", col=1, row=1, colspan=4)
        self.label5.configure(font=("Arial", 40))
        self.frame5.Seperator(col=1, row=2, colspan=4)
        self.receipt_text = self.frame5.Text("", col=1, row=3, colspan=4, sticky=N)

        self.frame5.Button('❮', lambda: nt[0].select(0), col=6, style='x.TButton')

        # Tab6
        self.denom_dict = {"5": 17, "10": 2, "50": 54, "100": 92, "500": 0, "1000": 1, "2000": 0, "5000": 12}
        self.frame6 = self.tab6.addFrame("Операционный день закрыт")
        self.label6 = self.frame6.Label("Операционный день закрыт", size=int(self.screen_pad * 0.8), col=0, row=0, colspan=4)
        self.label6.configure(foreground="#57c8ff")
        self.frame6.Seperator(col=0, row=2, colspan=4)
        self.denom_text = tkinter.Text(self.frame6.master, font=("Arial", int(self.screen_pad*0.3)),
                                       height=self.screen_pad*0.2, border=False)
        self.denom_text.tag_configure("center", justify='center')
        self.denom_text.grid(column=0, row=3, columnspan=4, sticky=N)
        self.frame6.Button('❮', lambda: nt[0].select(0), col=4, rowspan=4, style='x.TButton')

        # Tab7
        self.frame7 = self.tab7.addFrame("Операционный день открыт")
        self.label7 = self.frame7.Label("Операционный день открыт\nСчетчики обнулены"
                                        , size=int(self.screen_pad * 0.8), col=0, row=0,
                                        colspan=4)
        self.label7.configure(foreground="#57c8ff")
        self.frame7.Seperator(col=0, row=2, colspan=4)
        self.denom_text1 = tkinter.Text(self.frame7.master, font=("Arial", int(self.screen_pad * 0.3)),
                                       height=self.screen_pad * 0.2, border=False)
        self.denom_text1.tag_configure("center", justify='center')
        self.denom_text1.grid(column=0, row=3, columnspan=4, sticky=N)
        self.frame7.Button('❮', lambda: nt[0].select(0), col=4, rowspan=4, style='x.TButton')

        # Tab8
        frame8 = self.tab8.addFrame("Откройте смену")
        frame_msg = frame8.addLabelFrame("", colspan=4)
        label8 = frame_msg.Label("Операционный день закрыт.\n Для начала работы откройте\n операционный день."
                                 , size=int(self.screen_pad * 0.8))
        label8.configure(foreground="#57c8ff", justify="center")
        frame8.Button('❮', lambda: nt[0].select(0), col=4, style='x.TButton')


        #self.bool = tkinter.BooleanVar()
        #self.togglebutton = self.frame.ToggleButton(text="Toggle button", variable=self.bool)
        #self.frame.SlideSwitch("Switch", self.bool)
        #self.togglebutton.grid(row=2, column=2)
        self.run(onlyFrames=False)

    def day_close(self):
        if self.day_status:
            self.day_state(False)
            self.day_status = False
        self.denom_text.configure(state="normal")
        self.denom_text.delete("0.0", END)
        self.denom_text.insert(END, f"{datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\n{self.adres}В сумке:\n", "center")
        total = 0
        for denom, quantity in self.denom_dict.items():
            self.denom_text.insert(END, f"{denom} руб. - {quantity} шт.\n", "center")
            total += int(denom) * quantity
        self.denom_text.insert(END, f"ИТОГО {str(total)} руб.\n\n ОПЕРАЦИОННЫЙ ДЕНЬ ЗАКРЫТ", "center")
        self.denom_text.configure(state="disabled")
        nt[0].select(5)

    def day_open(self):
        if not self.day_status:
            self.day_state(True)
            self.day_status = True
        self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
        self.label7.configure(justify="center")
        self.denom_text1.configure(state="normal")
        self.denom_text1.delete("0.0", END)
        self.denom_text1.insert(END, f"{datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\n{self.adres}В сумке:\n", "center")
        for denom, quantity in self.denom_dict.items():
            self.denom_text1.insert(END, f"{denom} руб. - {quantity} шт.\n", "center")
        self.denom_text1.insert(END, "ОПЕРАЦИОННЫЙ ДЕНЬ ОТКРЫТ\nСЧЕТЧИКИ ОБНУЛЕНЫ", "center")
        self.denom_text1.configure(state="disabled")
        nt[0].select(6)


    def tree_selection(self, event):
        item = self.tree_data.item(self.tree_data.selection())
        self.client = item["text"]
        self.account = item["values"][0]

        # if not self.label:
        #     self.label = self.frame4.Text(f"{self.client} {self.account}", col=1, row=2, colspan=3, sticky=W)
        #     self.label.configure(font=("Arial", int(self.screen_pad*0.3)))
        #     self.frame4.Button('Подтвердить', lambda: nt[0].select(2), col=3, row=2, colspan=2, sticky=E)
        # else:
        #     self.label.configure(text=f"{self.client} {self.account}")

    def receipt(self):
        receipt_table = PrettyTable(["Время внесения", "Сумма"], border=False)
        receipt_table.add_row([datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"), "2000"])
        receipt_total = f"{self.adres}{self.receipt_number}\n{self.client}\n{self.account}\n\n{receipt_table}\n\n ИТОГО 2000"
        self.receipt_text.configure(text=receipt_total, font="Courier", justify="center")
        self.make_qr(receipt_total)
        self.print_text(receipt_total)
        self.print_qr("print_qr.png")
        self.print_text(f" \n \n \n \n  {'_'* 23}")
        img = ImageTk.PhotoImage(Image.open("tmpqr.png"))
        self.qr_label.configure(image=img)
        nt[0].select(4)

    def make_qr(self, qr_input):
        qr = qrcode.make(qr_input, box_size=3)
        qr_print = qrcode.make(qr_input, box_size=1)
        qr.save("tmpqr.png")
        qr_print.save("print_qr.png")

    def print_text(self, print_text):
        x = 0
        y = 30
        string = print_text.split("\n")
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.printer_name)
        hDC.StartDoc("Printing...")
        hDC.StartPage()
        for line in string:
            hDC.TextOut(x, y, line)
            y += 30
        hDC.EndPage()
        hDC.EndDoc()

    def print_qr(self, file_name):

        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.printer_name)
        printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
        printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps(PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

        bmp = Image.open(file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate(90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        hDC.StartDoc(file_name)
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

    def entry_insert(self, field: str):
        if field  == "user":
            self.user_field.delete(0, END)
            self.user_field.insert("0", "ЛОГИН")
        elif field == "pass":
            self.password_field.delete(0, END)
            self.password_field.configure(show="")
            self.password_field.insert("0", "ПАРОЛЬ")

    def clear_user_entry(self):
        self.user_field.focus_set()
        if self.user_field.get() == "ЛОГИН":
            self.user_field.delete(0, END)
        if self.password_field.get() == "":
            self.entry_insert("pass")
        self.edit_var = self.userinputvar

    def clear_password_entry(self):
        self.password_field.focus_set()
        print(str(self.root.focus_get()) == ".!notebook.!frame.!frame.!entry", str(self.root.focus_get()))
        if self.password_field.get() == "ПАРОЛЬ":
            self.password_field.delete(0, END)
            self.password_field.configure(show="✳")
        if self.user_field.get() == "":
            self.entry_insert("user")
        self.edit_var = self.passinputvar



    def backspace(self):
        text = self.edit_var.get()
        if text.isdigit():
            new_text = text[:-1]
            self.edit_var.set(new_text)
        print(self.passinputvar, self.userinputvar)
        if self.password_field.get() == "":
            self.entry_insert("pass")
        if self.user_field.get() == "":
            self.entry_insert("user")

    def set_defoult_entry(self):
        self.user_field.delete(0, END)
        self.user_field.insert(0, "ЛОГИН")
        self.password_field.delete(0, END)
        self.password_field.insert(0, "ПАРОЛЬ")
        self.password_field.configure(show="")

    def authorization(self):
        input_user = self.userinputvar.get()
        input_pass = self.passinputvar.get()
        if input_user == "1" and input_pass == "1":
            self.set_defoult_entry()
            if self.day_status:
                nt[0].select(3)
            else:
                nt[0].select(7)
        elif input_user == "2" and input_pass == "2":
            self.set_defoult_entry()
            nt[0].select(1)

        else:
            self.flash()
            self.root.update_idletasks()
            time.sleep(0.1)
            self.flash()

    def flash(self):
        current_color = self.user_field.cget("foreground")
        if str(current_color) == "red":
            next_color = "white"
        else:
            next_color = "red"
        self.user_field.config(foreground=next_color)
        self.password_field.config(foreground=next_color)

    def digit_buttons(self, current_button):
        text = self.edit_var.get()
        text += current_button.cget("text")
        self.edit_var.set(text)

    def day_state(self, status):
        with open("variables.py", "w") as f:
            if not status:
                f.write("day_state = False")
            else:
                f.write("day_state = True")


if __name__ == '__main__':
    App()
