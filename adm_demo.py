import sys
from subprocess import call
import json
import threading
import TKinterModernThemes as Tkm
import qrcode
import tkinter
import keyboard
import datetime
from prettytable import PrettyTable
from PIL import ImageTk
from PIL import Image as Pic
from PIL import ImageWin
import win32print
import win32ui
from models import get_user
from passlib.apps import custom_app_context as pwd_context
import pyAesCrypt
from engine import *
from constants import *
from struct import unpack
from load import *
from multiprocessing import Process, freeze_support
from subprocess import Popen


def crypt(file, passwor):
    buffer_size = 256 * 512
    pyAesCrypt.encryptFile(str(file), str(file) + ".crp", passwor, buffer_size)
    # print("[Encrypt] '" + str(file) + ".crp'")
    os.remove(file)


def decrypt(file, passwor):
    buffer_size = 256 * 512
    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]), passwor, buffer_size)
    # print("[Decrypt] '" + str(os.path.splitext(file)[0]) + "'")
    os.remove(file)


def restart_program():
    # restart the current program
    python = sys.executable
    call([python, __file__])
    sys.exit()


class App(Tkm.ThemedTKinterFrame):
    def __init__(self):
        self.data = self.json_read()
        theme = self.data[2]["theme"]
        mode = self.data[2]["mode"]
        Tkm.firstWindow = True  # when change theme must be top-level window
        super().__init__("ADM_show", theme, mode, useconfigfile=False)  # azure / sun-valley / park
        print("start")
        self.root.iconbitmap(default='adm.ico')
        keyboard.add_hotkey("enter", lambda: self.enter_key())
        self.client = ""
        self.account = ""
        self.img = None
        self.count = 0
        self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "200": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
        self.count_event_flag = False
        self.day_status = self.data[0]["day_state"]
        self.receipt_number = int(self.data[0]['receipt_number'])
        self.del_flag = True
        self.printer_name = win32print.GetDefaultPrinter()  # "KPOS_58 Printer"
        self.edit_var = tkinter.StringVar()

        if theme == "azure" or theme == "sun-valley":
            self.theme_color = '#57c8ff'
        else:
            self.theme_color = "#217346"

        if mode == "light":
            self.theme_foreground = "black"
        else:
            self.theme_foreground = "white"

        self.adres = "АДМ №213445 121096\nг.Москва\nул.Кастанаевская, д.24 \nEMAIL: sales@deep2000.ru\n"
        self.label = None
        self.screen_pad = self.root.winfo_screenwidth() * 0.05

        # Global styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Arial", int(self.screen_pad*0.9), "bold"), justify='center')
        self.style.configure('accept.TButton', font=("Arial", int(self.screen_pad * 0.9), "bold"), justify='center',
                             foreground="red")
        self.style.configure('x.TButton', font=("Arial", int(self.screen_pad*0.5), "bold"), foreground="red")
        self.style.configure('Treeview', font=("Arial", int(self.screen_pad*0.55)), rowheight=75)
        self.style.configure('Treeview.Heading', font=("Arial", 40))
        self.style.map('Treeview', background=[('selected', self.theme_color)], foreground=[('selected', 'black')])
        self.style.configure('TEntry', font=("Arial", int(self.screen_pad * 0.3)))
        if mode == "light":
            self.style.configure('TFrame', borderwidth=3, relief='ridge')  # flat,groove,raised,ridge,solid,or sunken
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

        self.button1 = self.frame1.Button("1", lambda: self.digit_buttons("1"), col=0, row=2)
        self.button2 = self.frame1.Button("2", lambda: self.digit_buttons("2"), col=1, row=2)
        self.button3 = self.frame1.Button("3", lambda: self.digit_buttons("3"), col=2, row=2)
        self.button4 = self.frame1.Button("4", lambda: self.digit_buttons("4"), col=0, row=3)
        self.button5 = self.frame1.Button("5", lambda: self.digit_buttons("5"), col=1, row=3)
        self.button6 = self.frame1.Button("6", lambda: self.digit_buttons("6"), col=2, row=3)
        self.button7 = self.frame1.Button("7", lambda: self.digit_buttons("7"), col=0, row=4)
        self.button8 = self.frame1.Button("8", lambda: self.digit_buttons("8"), col=1, row=4)
        self.button9 = self.frame1.Button("9", lambda: self.digit_buttons("9"), col=2, row=4)
        self.button0 = self.frame1.Button("0", lambda: self.digit_buttons("0"), col=1, row=5)
        self.button0.configure(width=5)

        self.button_del = self.frame1.AccentButton("УДАЛ", command=lambda: ..., col=0, row=5)
        self.button_del.bind("<ButtonRelease>", self.del_released)
        self.button_del.bind("<ButtonPress>", self.del_pressed)
        self.enter = self.frame1.AccentButton("ВВОД", self.authorization, col=2, row=5)
        self.enter.focus_set()

        # Tab2
        frame2 = self.tab2.addFrame("Инкассация")
        frame2.AccentButton("Открытие\nоперационного дня", self.day_open,
                            col=0, row=0, colspan=4, padx=self.screen_pad/2, pady=self.screen_pad/2)
        frame2.Button("Закрытие\nоперационного дня", self.day_close,
                      col=0, row=1, colspan=4, padx=self.screen_pad/2, pady=self.screen_pad/2)
        back = frame2.Button('❮', lambda: self.select_tab(0), col=4, rowspan=2,  style='x.TButton')
        back.configure(width=1)

        # Tab3
        frame3 = self.tab3.addFrame("Внесение")
        deposit_frame = frame3.addLabelFrame("", col=0, row=2,)
        denom_frame = frame3.addLabelFrame("", col=0, row=0, rowspan=2)
        button_frame = frame3.addFrame(name="", col=2, row=1, rowspan=2)
        self.label_denoms = denom_frame.Label(text=self.dict_to_text(self.denom_dict)[0], col=0)
        self.label_quantity = denom_frame.Label(text=self.dict_to_text(self.denom_dict)[1], col=1)
        self.label_deposit = deposit_frame.Label(text=self.count, col=0, row=1)
        self.label_deposit.configure(font=("Arial", int(self.screen_pad), "bold"), justify="center")

        self.label_denoms.configure(font=("Arial", int(self.screen_pad*0.45), "bold"), width=12, justify="right",
                                    foreground=self.theme_color)
        self.label_quantity.configure(font=("Arial", int(self.screen_pad * 0.45), "bold"), width=12, justify="left")

        label_down = frame3.Label("Внесите банкноты.\nМаксимальное\nколличество-\n200 банкнот", col=2, row=0)
        label_down.configure(font=("Arial", int(self.screen_pad*0.6), "bold"),
                             foreground=self.theme_color, justify="center")
        self.done = button_frame.Button('Зачислить', self.receipt)
        self.back_button = frame3.Button('❮', lambda: self.select_tab(3), col=3, rowspan=3, style='x.TButton')
        self.back_button.configure(width=1)

        # Tab4
        self.frame4 = self.tab4.addFrame("Выбор счета")
        label_up = self.frame4.Label("Выберете счет для зачисления", col=0, row=0, colspan=7)
        label_up.configure(font=("Arial", int(self.screen_pad * 0.8), "bold"), foreground=self.theme_color)
        self.tree_data = self.frame4.Treeview(['Контрагент', 'Счет'], [110, 140], 3, [{"name": "", "purpose": ""}],
                                              'subfiles', ['name', 'purpose'], col=0, row=1, colspan=7, rowspan=7)
        self.tree_data.configure(style="Treeview")
        self.tree_data.bind("<<TreeviewSelect>>", self.tree_selection)
        back = self.frame4.Button('❮', lambda: self.select_tab(0), col=7, rowspan=9, style='x.TButton')
        back.configure(width=1)
        self.accept_button = self.frame4.Button(text="Выбрать", col=0, row=8, colspan=7, command=self.deposit_start)

        # Tab5
        self.frame5 = self.tab5.addFrame("Заберите чек")
        self.frame5.Label(text="", col=0, padx=self.screen_pad)
        self.qr_label = ttk.Label(self.frame5.master)
        self.qr_label.grid(row=1, column=3, columnspan=2)
        self.label5 = self.frame5.Label("Заберите чек", col=1, row=0, colspan=4)
        self.label5.configure(font=("Arial", int(self.screen_pad * 0.8)))
        self.receipt_text = self.frame5.Text("", col=1, row=1, colspan=2, sticky=N)
        back = self.frame5.Button('❮', lambda: self.select_tab(0), col=9, style='x.TButton', rowspan=7)
        back.configure(width=1)

        # Tab6
        self.frame6 = self.tab6.addFrame("Операционный день закрыт")
        self.label6 = self.frame6.Label("Операционный день закрыт", size=int(self.screen_pad * 0.8), col=0,
                                        row=0, colspan=4)
        self.label6.configure(foreground=self.theme_color)
        self.frame6.Seperator(col=0, row=1, colspan=4)
        self.denom_text = tkinter.Text(self.frame6.master, font=("Arial", int(self.screen_pad*0.25)),
                                       border=False)
        self.denom_text.tag_configure("center", justify='center')
        self.denom_text.grid(column=0, row=2, columnspan=4, rowspan=4, sticky=N)
        back = self.frame6.Button('❮', lambda: self.select_tab(0), col=4, rowspan=6, style='x.TButton')
        back.configure(width=1)

        # Tab7
        self.frame7 = self.tab7.addFrame("Операционный день открыт")
        self.label7 = self.frame7.Label("Операционный день открыт", size=int(self.screen_pad * 0.8), col=0, row=0,
                                        colspan=4, pady=0)
        self.label7.configure(foreground=self.theme_color)
        self.frame7.Seperator(col=0, row=1, colspan=4)
        self.denom_text1 = tkinter.Text(self.frame7.master, font=("Arial", int(self.screen_pad * 0.25)),
                                        border=False)
        self.denom_text1.tag_configure("center", justify='center')
        self.denom_text1.grid(column=0, row=2, columnspan=4, rowspan=4)
        back = self.frame7.Button('❮', lambda: self.select_tab(0), col=4, rowspan=6, style='x.TButton')
        back.configure(width=1)

        # Tab8
        frame8 = self.tab8.addFrame("Откройте смену")
        frame_msg = frame8.addLabelFrame("", colspan=4)
        label8 = frame_msg.Label("Операционный день закрыт.\n Для начала работы откройте\n операционный день.",
                                 size=int(self.screen_pad * 0.8))
        label8.configure(foreground=self.theme_color, justify="center")
        back = frame8.Button('❮', lambda: self.select_tab(0), col=4, style='x.TButton')
        back.configure(width=1)

        self.engine = Engine()
        self.engine.power_on_0ff(TURN_ON)
        self.port = self.engine.validator_init()
        self.root.withdraw()
        self.root.after(1000, self.show)
        print("finish")
        self.run(onlyFrames=False)

    def show(self):
        self.root.deiconify()

    def finish_load(self):
        Popen(f"taskkill /F /PID {self.data[0]['load_pid']}")

    def day_close(self):
        if self.day_status:
            self.day_state(False)
            self.day_status = False
        self.denom_text.configure(state="normal")
        self.denom_text.delete("0.0", END)
        self.denom_text.insert(END, f"{datetime.now().strftime('%Y-%m-%d %H.%M.%S')}\n{self.adres}В сумке:\n", "center")
        for denom, quantity in self.data[1].items():
            self.denom_text.insert(END, f"{denom} руб. - {quantity} шт.\n", "center")
        self.denom_text.insert(END, f"\nИТОГО {str(self.data[0]['day_counter'])} руб.\nОПЕРАЦИОННЫЙ ДЕНЬ\nЗАКРЫТ", "center")
        self.denom_text.configure(state="disabled")
        self.print_text(self.denom_text.get("0.0", END))
        self.print_text(f" \n \n \n \n  {'_' * 23}")
        self.select_tab(5)

    def day_open(self):
        if not self.day_status:
            self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "200": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
            self.day_state(True)
            self.data[0]["day_counter"] = 0
            self.data[1] = self.denom_dict
            self.json_write(self.data)
            self.day_status = True
        self.label7.configure(justify="center")
        self.denom_text1.configure(state="normal")
        self.denom_text1.delete("0.0", END)
        self.denom_text1.insert(END, f"{datetime.now().strftime('%Y-%m-%d %H.%M.%S')}"
                                     f"\n{self.adres}В сумке:\n", "center")
        for denom, quantity in self.denom_dict.items():
            self.denom_text1.insert(END, f"{denom} руб. - {quantity} шт.\n", "center")
        self.denom_text1.insert(END, "ОПЕР. ДЕНЬ ОТКРЫТ\nСЧЕТЧИКИ ОБНУЛЕНЫ", "center")
        self.denom_text1.configure(state="disabled")
        self.print_text(self.denom_text1.get("0.0", END))
        self.print_text(f" \n \n \n \n  {'_' * 23}")
        self.select_tab(6)

    def current_tab(self):
        print(self.root.winfo_ismapped())
        return self.notebook.notebook.tabs().index(self.notebook.notebook.select())

    def select_tab(self, tab):
        self.notebook.notebook.select(tab)

    def tree_selection(self, event):
        item = self.tree_data.item(self.tree_data.selection())
        self.client = item["text"]
        self.account = item["values"][0]

    def update_counters(self):
        self.data[0]["day_counter"] += self.count
        for denom in self.data[1].keys():
            self.data[1][denom] += self.denom_dict[denom]
        self.json_write(self.data)

    def receipt(self):
        self.label_quantity.configure(text=self.dict_to_text(self.denom_dict)[1])
        self.label_deposit.configure(text=self.count)
        self.update_counters()
        self.back_button.configure(state="normal")
        date = datetime.now().strftime("%Y.%m.%d\n%H:%M:%S")
        receipt_table = PrettyTable(["Время внесения", "Сумма"], border=False)
        receipt_table.add_row([date, self.count])
        receipt_table.add_row(["\n"+self.dict_to_text(self.denom_dict)[0], "\n"+self.dict_to_text(self.denom_dict)[1]])
        receipt_table.add_row(["ИТОГО", self.count])
        receipt_total = f"Чек № {self.receipt_number}\n{self.adres}{self.client}\n{self.account}\n\n{receipt_table}"
        receipt_qr = f"Чек № {self.receipt_number}\n{self.adres}{self.client}\n{self.account}\n{date}" \
                     f"\nИТОГО {self.count}"
        self.receipt_number += 1
        self.data[0]["receipt_number"] = int(self.data[0]["receipt_number"]) + 1
        self.json_write(self.data)
        self.receipt_text.configure(text=receipt_total, font="Courier", justify="center")
        self.make_qr(receipt_qr)
        self.print_text(receipt_total)
        self.print_qr("print_qr.png")
        self.print_text(f" \n \n \n \n  {'_'* 23}")
        photo = Pic.open("tmpqr.png")
        img = ImageTk.PhotoImage(photo)
        self.qr_label.configure(image=img)
        self.select_tab(4)
        self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "200": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
        self.count = 0

    def make_qr(self, qr_input):
        qr = qrcode.make(qr_input, box_size=3)
        qr_print = qrcode.make(qr_input, box_size=1)
        qr.save("tmpqr.png")
        qr_print.save("print_qr.png")

    def print_text(self, print_text):
        x = 0
        y = 30
        string = print_text.split("\n")
        h_dc = win32ui.CreateDC()
        h_dc.CreatePrinterDC(self.printer_name)
        h_dc.StartDoc("Printing...")
        h_dc.StartPage()
        for line in string:
            h_dc.TextOut(x, y, line)
            y += 30
        h_dc.EndPage()
        h_dc.EndDoc()

    def print_qr(self, file_name):

        h_dc = win32ui.CreateDC()
        h_dc.CreatePrinterDC(self.printer_name)
        printable_area = h_dc.GetDeviceCaps(HORZRES), h_dc.GetDeviceCaps(VERTRES)
        printer_size = h_dc.GetDeviceCaps(PHYSICALWIDTH), h_dc.GetDeviceCaps(PHYSICALHEIGHT)
        printer_margins = h_dc.GetDeviceCaps(PHYSICALOFFSETX), h_dc.GetDeviceCaps(PHYSICALOFFSETY)

        bmp = Pic.open(file_name)
        if bmp.size[0] > bmp.size[1]:
            bmp = bmp.rotate(90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        h_dc.StartDoc(file_name)
        h_dc.StartPage()

        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height
        dib.draw(h_dc.GetHandleOutput(), (x1, y1, x2, y2))

        h_dc.EndPage()
        h_dc.EndDoc()
        h_dc.DeleteDC()

    def entry_insert(self, field: str):
        if field == "user":
            self.user_field.delete(0, END)
            self.user_field.insert("0", "ЛОГИН")
        elif field == "pass":
            self.password_field.delete(0, END)
            self.password_field.configure(show="")
            self.password_field.insert("0", "ПАРОЛЬ")

    def clear_user_entry(self):
        self.user_field.focus_set()
        if "ЛОГИН" in self.user_field.get():
            self.user_field.delete(0, END)
        if self.password_field.get() == "":
            self.entry_insert("pass")
        self.edit_var = self.userinputvar

    def clear_password_entry(self):
        self.password_field.focus_set()
        if "ПАРОЛЬ" in self.password_field.get():
            self.password_field.delete(0, END)
            self.password_field.configure(show="✳")
        if self.user_field.get() == "":
            self.entry_insert("user")
        self.edit_var = self.passinputvar

    def backspace(self):
        if self.del_flag:
            text = self.edit_var.get()
            if text.isdigit():
                new_text = text[:-1]
                self.edit_var.set(new_text)
            if self.password_field.get() == "":
                self.entry_insert("pass")
            if self.user_field.get() == "":
                self.entry_insert("user")
            threading.Timer(0.3, lambda: self.backspace()).start()

    def del_released(self, event):
        self.del_flag = False

    def del_pressed(self, event):
        self.del_flag = True
        self.backspace()

    def set_default_entry(self):
        self.user_field.delete(0, END)
        self.user_field.insert(0, "ЛОГИН")
        self.password_field.delete(0, END)
        self.password_field.insert(0, "ПАРОЛЬ")
        self.password_field.configure(show="")

    def port_close(self):
        if self.port.is_open:
            self.port.close()

    def change_theme(self,theme,mode):
        self.port_close()
        self.data[2]["theme"] = theme
        self.data[2]["mode"] = mode
        self.json_write(self.data)
        self.handleExit()
        restart_program()

    def authorization(self):
        input_user = self.userinputvar.get()
        input_pass = self.passinputvar.get()
        # Work with db
        user = get_user(input_user)
        if user:
            user_dict = user.to_dict()
            if user_dict["status"] == "Кассир":
                password_hash = user_dict["password"]
                if pwd_context.verify(input_pass, password_hash):
                    self.set_default_entry()
                    if self.day_status:
                        for i in self.tree_data.get_children():
                            self.tree_data.delete(i)
                        for data in user.client:
                            tree_row = data.to_dict()
                            self.tree_data.insert('', 'end',  text=tree_row["name"], values=tree_row["purpose"])
                        self.select_tab(3)
                        self.tree_data.selection_add(self.tree_data.get_children()[0])
                    else:
                        self.select_tab(7)
                else:
                    self.flashing()

            elif user_dict["status"] == "Инкассатор":
                password_hash = user_dict["password"]
                if pwd_context.verify(input_pass, password_hash):
                    self.set_default_entry()
                    self.select_tab(1)
                else:
                    self.flashing()

            elif user_dict["status"] == "Об авторах":
                password_hash = user_dict["password"]
                if pwd_context.verify(input_pass, password_hash):
                    self.easter_egg(input_pass)
                else:
                    self.flashing()

        elif input_user == "3" and input_pass == "3":
            self.change_theme("azure", "light")
        elif input_user == "4" and input_pass == "4":
            self.change_theme("park", "light")
        elif input_user == "5" and input_pass == "5":
            self.change_theme("park", "dark")
        elif input_user == "6" and input_pass == "6":
            self.change_theme("sun-valley", "dark")
        elif input_user == "31" and input_pass == "31":
            self.engine.power_on_0ff(TURN_OFF)
        elif input_user == "32" and input_pass == "32":
            self.engine.power_on_0ff(TURN_ON)
            self.engine.validator_init()
        elif input_user == "55" and input_pass == "55":
            self.engine.send_to_port(CMD_B5)
            time.sleep(0.1)
            self.engine.send_to_port(RESP_B5)
        elif input_user == "03" and input_pass == "03":
            self.port.close()
            self.handleExit()
        else:
            self.flashing()

    def flashing(self):
        self.flash(self.user_field, self.password_field)
        self.root.update_idletasks()
        time.sleep(0.1)
        self.flash(self.user_field, self.password_field)

    def flash(self, field, field1):
        current_color = self.user_field.cget("foreground")
        if str(current_color) == "red":
            next_color = self.theme_foreground
        else:
            next_color = "red"
        field.config(foreground=next_color)
        field1.config(foreground=next_color)

    def digit_buttons(self, digit):
        if self.edit_var.get().isdigit() or self.edit_var.get() == "":
            text = self.edit_var.get()
            text += digit
            self.edit_var.set(text)

    def day_state(self, status):
        all_variables = self.json_read()
        if not status:
            all_variables[0]["day_state"] = False
            all_variables[0]["receipt_number"] = 1
        else:
            all_variables[0]["day_state"] = True
        self.json_write(all_variables)

    def json_read(self):
        with open("variables.json", "r", encoding="utf-8") as f:
            all_variables = json.load(f)
            return all_variables

    def json_write(self, data):
        with open("variables.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def easter_egg(self, password):
        if os.path.isfile("ficha.png.crp"):
            decrypt("ficha.png.crp", password)
        self.img = tkinter.PhotoImage(file="ficha.png")
        window = tkinter.Toplevel(borderwidth=20)  # Создаём всплывающее окно
        window.title("О создателях")
        window.grab_set()
        top_level_label = ttk.Label(window, image=self.img)
        top_level_label.grid(column=0, row=0)
        close_buttton = ttk.Button(window, text="ЗАКРЫТЬ", command=lambda: window.destroy())
        close_buttton.grid(column=0)
        crypt("ficha.png", password)

    def dict_to_text(self, dct):
        text_values = ""
        text_keys = ""
        for key, value in dct.items():
            text_values += f"{value} шт.\n"
            text_keys += f"{key} руб.\n"
        return text_keys, text_values

    def deposit_start(self):
        self.count = 0
        try:
            self.select_tab(2)
            self.read_data_from_port()
            self.state_butons_config("disable", "normal")
        except Exception as e:
            self.engine.write_logs("a+", f"\n{e}")
            self.accept_button.configure(style="accept.TButton")
            self.root.update_idletasks()
            time.sleep(0.3)
            self.accept_button.configure(style="TButton")

    def start(self):
        self.engine.send_to_port(CMD_B1)
        self.engine.send_to_port(CMD_B2)

    def state_butons_config(self, state_done, state_back):
        self.done.configure(state=state_done)
        self.back_button.configure(state=state_back)

    def read_data_from_port(self):
        if self.current_tab() == 2:
            self.port.flush()
            if self.count_event_flag:
                data = self.port.read(64)
            else:
                data = self.port.read_until("\n")
            len_data = len(data)
            data_hex = binascii.hexlify(data)
            event = data_hex[4:6]
            error_hex = data_hex[120:122]
            denom_byte = data[52:54]
            reject_reason = data_hex[16:20]
            chain_indicator = data_hex[20:120]

            if len_data > 0:
                # print(f"Ответ  {binascii.hexlify(data)}", f"{self.count_event_flag}\n")
                if event == b"48":  # Реакция на 48 событие ПОЛУЧЕН ОТЧЕТ ОБ ОШИБКЕ
                    self.port.write(RESP_48)
                if event == b"21":  # Реакция Hoper on событие
                    self.count_event_flag = True
                    self.start()
                    self.state_butons_config("disable", "disable")
                    self.port.write(RESP_HOP_ON)
                if event == b"22":  # Реакция Hoper off событие
                    self.port.write(RESP_HOP_OFF)
                    self.count_event_flag = False
                    if self.count != 0:
                        self.state_butons_config("normal", "disable")
                    else:
                        self.state_butons_config("disable", "normal")
                if event == b"28":  # Реакция Banknotes don't Exist Reject событие
                    self.port.write(RESP_REJ_OFF)
                if event == b"27":  # Реакция на Banknotes Exist on Reject событие
                    self.port.write(RESP_REJ_ON)
                if event == b"41":  # Реакция Send SC initialize Status & Result событие ПРИНЯТ ОТЧЁТ О СБРОСЕ ОШИБОК
                    self.port.write(RESP_B5)
                if event == b"24":  # Реакция Send Counting Result событие (данные просчета)
                    self.port.write(RESP_24)
                if event == b"45":  # Реакция Deposit Ready Status событие
                    self.port.write(RESP_45)

                if len_data == 64 and event == b"23" and error_hex == b"00":  # if count event and there is no error
                    self.event_23(denom_byte)
                if event == b"23" and chain_indicator == b'00' * 50:
                    self.engine.write_logs("a+", "Insert chain detected")

                if error_hex in REJECT_GROUP.keys() and reject_reason != b"0000" and event != b'24':
                    for error_text, error_code in RECO_ERROR.items():
                        if reject_reason == error_code:
                            self.engine.write_logs("a+", error_text)

            threading.Timer(0.06, self.read_data_from_port).start()

    def event_23(self, denom_byte):
        nominal = unpack("<h", denom_byte)  # little-endian
        self.denom_dict[str(nominal[0])] += 1
        self.count += nominal[0]

        self.label_quantity.configure(text=self.dict_to_text(self.denom_dict)[1])
        self.label_deposit.configure(text=self.count)

    def enter_key(self):
        tab = self.current_tab()
        if tab == 0:
            self.authorization()
        if tab == 3:
            self.deposit_start()


def load():
    Load()


if __name__ == '__main__':
    freeze_support()
    process1 = Process(target=load)
    process1.start()
    a = App()
    process1.terminate()
    a.root.mainloop()
