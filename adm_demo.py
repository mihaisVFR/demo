from sys import exit as sys_exit
from sys import executable as sys_executable
from subprocess import call
from json import load, dump
from threading import Timer as threading_Timer
import TKinterModernThemes as Tkm
# from qrcode import make as qrcode_make
import tkinter
from prettytable import PrettyTable
# from PIL import Image as Pic
# from PIL import ImageWin
# from win32print import GetDefaultPrinter
# from win32ui import CreateDC as win32ui_CreateDC
from models import get_user
from passlib.apps import custom_app_context as pwd_context
from pyAesCrypt import encryptFile, decryptFile
from engine import *
# from constants import *
from struct import unpack
from load import *
from multiprocessing import Process, freeze_support
from printer import *


def crypt(file, password):
    buffer_size = 256 * 512
    encryptFile(str(file), str(file) + ".crp", password, buffer_size)
    os.remove(file)


def decrypt(file, password):
    buffer_size = 256 * 512
    decryptFile(str(file), str(os.path.splitext(file)[0]), password, buffer_size)
    os.remove(file)


def restart_program():
    # restart the current program
    python = sys_executable
    call([python, __file__])
    sys_exit()


def loading():
    Load()


class App(Tkm.ThemedTKinterFrame):
    """Demonstration of the deposit machine KDS200. Include GUI, authorization ,
    read from com port and print function"""
    def __init__(self):

        self.data = self.json_read()
        self.theme = self.data[2]["theme"]
        self.mode = self.data[2]["mode"]
        Tkm.firstWindow = True  # when change theme must be root window

        super().__init__("ADM_show", self.theme, self.mode, useconfigfile=False)  # azure / sun-valley / park

        self.root.bind("<Return>", self.enter_key)
        self.root.iconbitmap(default='adm.ico')
        self.timer = None  # timer of screensaver
        self.client = ""  # user data
        self.account = ""  # user account
        self.img = None  # qr code image print size
        self.image_qr = None  # qr code image label size
        self.count = 0  # quantity of count notes
        self.denom_dict = {"5": 0, "10": 0, "50": 0, "100": 0, "200": 0, "500": 0, "1000": 0, "2000": 0, "5000": 0}
        self.count_event_flag = False  # flag of count event
        self.day_status = self.data[0]["day_state"]  # bank day status
        self.receipt_number = int(self.data[0]['receipt_number'])
        self.del_flag = True  # if button pressed backspace foo repeat
        self.adres = "АДМ №213445 121096\nг.Москва\nул.Кастанаевская, д.24 \nEMAIL: sales@deep2000.ru\n"

        # self.printer_name = GetDefaultPrinter()  # "KPOS_58 Printer"
        # self.print_separator = f" \n \n \n \n  {'_' * 23}"

        self.user_text = tkinter.StringVar()
        self.password_text = tkinter.StringVar()
        self.screen_pad = self.root.winfo_screenwidth() * 0.05

        # set foreground for switch color themes
        if self.theme == "azure" or self.theme == "sun-valley":
            self.theme_color = '#57c8ff'
        else:
            self.theme_color = "#217346"

        if self.mode == "light":
            self.theme_foreground = "black"
        else:
            self.theme_foreground = "white"

        # Global styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Arial", int(self.screen_pad*0.9), "bold"), justify='center')
        self.style.configure('eye.TButton', font=("Arial", int(self.screen_pad * 0.7), "bold"), justify='center')
        self.style.configure('park.TButton', font=("Arial", int(self.screen_pad * 0.5), "bold"), justify='center',
                             foreground="red", width=1)
        self.style.map('park.TButton', foreground=[('disabled', '#706f6f')])
        self.style.configure('accept.TButton', font=("Arial", int(self.screen_pad * 0.9), "bold"), justify='center',
                             foreground="red")
        self.style.configure('x.TButton', font=("Arial", int(self.screen_pad*0.5), "bold"), foreground="red", width=1)
        self.style.configure('Treeview', font=("Arial", int(self.screen_pad*0.55)), rowheight=75)
        self.style.configure('Treeview.Heading', font=("Arial", 40))
        self.style.map('Treeview', background=[('selected', self.theme_color)], foreground=[('selected', 'black')])
        self.style.configure('TEntry',  font=("Arial", int(self.screen_pad * 0.3)))
        if self.mode == "light":
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
        self.tab9 = self.notebook.addTab("ScreenSaver")

        # Tab1 #
        self.frame1 = self.tab1.addFrame("-")
        self.frame1.Label("ЛОГИН", int(self.screen_pad * 0.7), "bold", col=0, row=0)
        self.frame1.Label("ПАРОЛЬ", int(self.screen_pad * 0.7), "bold", col=0, row=1)
        entry_kwargs = {"font": ("Arial", int(self.screen_pad * 0.7), "bold"), "width": 7}
        self.user_field = self.frame1.Entry(textvariable=self.user_text, col=1, row=0, widgetkwargs=entry_kwargs)
        self.user_field.bind("<1>", self.set_user_entry)
        self.edit_field = self.user_field  # first insert user
        entry_kwargs["show"] = "✳"         # hide password
        self.password_field = self.frame1.Entry(textvariable=self.password_text,
                                                col=1, row=1, widgetkwargs=entry_kwargs)
        self.password_field.bind("<1>", self.set_password_entry)

        # create digit buttons
        btn_kwargs = {"takefocus": 0}
        grid_kwargs = ((1, 5), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3), (0, 4), (1, 4), (2, 4))
        for i in range(10):
            self.frame1.Button(str(i), command=lambda digit=i: self.digit_buttons(digit),
                               col=grid_kwargs[i][0], row=grid_kwargs[i][1], widgetkwargs=btn_kwargs)

        self.enter = self.frame1.AccentButton("ВВОД", lambda: self.enter_key(1), col=2, row=5, widgetkwargs=btn_kwargs)
        self.frame1.Button("👁", self.show_pass, col=2, row=1, sticky="w",
                           style="eye.TButton", widgetkwargs={"width": 2, "takefocus": 0})

        # bind events for restart screensaver timer
        for widget in self.frame1.widgets:
            if "Button" in str(widget):
                widget.widget.bind("<ButtonPress>", self.restart_screensaver)
        for key in range(10):
            self.root.bind(f"<KeyRelease-{key}>", self.restart_screensaver)

        self.button_del = self.frame1.AccentButton("УДАЛ", command=lambda: ..., col=0, row=5, widgetkwargs=btn_kwargs)
        self.button_del.bind("<ButtonRelease>", self.del_released)
        self.button_del.bind("<ButtonPress>", self.del_pressed)
        self.user_field.focus_set()

        # Tab2 #
        kwargs = {"state": "normal"}, {"state": "disable"}
        if self.data[0]["day_state"]:
            kwargs = kwargs[::-1]
        frame2 = self.tab2.addFrame("Инкассация")
        self.open_button = frame2.AccentButton("Открытие\nоперационного дня", self.day_open, col=0, row=0, colspan=4,
                                               padx=self.screen_pad/2, pady=self.screen_pad/2, widgetkwargs=kwargs[0])
        self.close_button = frame2.AccentButton("Закрытие\nоперационного дня", self.day_close, col=0, row=1, colspan=4,
                                                padx=self.screen_pad/2, pady=self.screen_pad/2, widgetkwargs=kwargs[1])
        frame2.Button('❮', lambda: self.select_tab(0), col=4, rowspan=2,  style='x.TButton')

        # Tab3 #
        frame3 = self.tab3.addFrame("Внесение")
        deposit_frame = frame3.addLabelFrame("", col=0, row=2,)
        denom_frame = frame3.addLabelFrame("", col=0, row=0, rowspan=2)
        button_frame = frame3.addFrame(name="", col=2, row=1, rowspan=2)
        self.label_denoms = denom_frame.Label(self.dict_to_text(self.denom_dict)[0], int(self.screen_pad*0.45),
                                              "bold", col=0, widgetkwargs={"width": 12, "justify": "right",
                                                                           "foreground": self.theme_color})
        self.label_quantity = denom_frame.Label(self.dict_to_text(self.denom_dict)[1], int(self.screen_pad * 0.45),
                                                "bold", col=1, widgetkwargs={"width": 12, "justify": "right"})
        self.label_deposit = deposit_frame.Label(self.count, int(self.screen_pad), "bold",
                                                 col=0, row=1, widgetkwargs={"justify": "center"})

        frame3.Label("Внесите банкноты.\nМаксимальное\nколичество-\n200 банкнот", int(self.screen_pad*0.6), "bold",
                     col=2, row=0, widgetkwargs={"justify": "center", "foreground": self.theme_color})

        # theme widget options
        if self.theme == "park" and self.mode == "dark":
            self.done = button_frame.AccentButton('Зачислить', self.receipt)
            self.back_button = frame3.Button('❮', lambda: self.select_tab(3), col=3, rowspan=3, style="park.TButton")
        else:
            self.done = button_frame.Button('Зачислить', self.receipt)
            self.back_button = frame3.Button('❮', lambda: self.select_tab(3), col=3, rowspan=3, style='x.TButton')

        # Tab4 #
        self.frame4 = self.tab4.addFrame("Выбор счета")
        self.frame4.Label("Выберете счет для зачисления", int(self.screen_pad * 0.8), "bold",  col=0, row=0, colspan=7,
                          widgetkwargs={"foreground": self.theme_color})
        self.tree = self.frame4.Treeview(['Контрагент', 'Счет'], [110, 140], 3, [{"name": "", "purpose": ""}],
                                         'subfiles', ['name', 'purpose'], col=0, row=1, colspan=7, rowspan=7,
                                         widgetkwargs={"style": "Treeview"})
        self.tree.bind("<<TreeviewSelect>>", self.tree_selection)
        self.frame4.Button('❮', lambda: self.select_tab(0), col=7, rowspan=9, style='x.TButton')
        self.accept_button = self.frame4.Button(text="Выбрать", col=0, row=8, colspan=7, command=self.deposit_start)

        # Tab5 #
        self.frame5 = self.tab5.addFrame("Заберите чек")
        self.frame5.Label(text="", col=0, padx=self.screen_pad)
        self.qr_label = ttk.Label(self.frame5.master, image=self.image_qr)
        self.qr_label.grid(row=1, column=3, columnspan=2)
        self.label5 = self.frame5.Label("Заберите чек", int(self.screen_pad * 0.8), col=1, row=0, colspan=4,
                                        widgetkwargs={"foreground": self.theme_color})
        self.receipt_text = self.frame5.Text("", col=1, row=1, colspan=2, sticky="n")
        self.frame5.Button('❮', lambda: self.select_tab(0), col=9, style='x.TButton', rowspan=7)

        # Tab6 #
        self.frame6 = self.tab6.addFrame("Операционный день закрыт")
        self.label6 = self.frame6.Label("Операционный день закрыт", size=int(self.screen_pad * 0.8), col=0,
                                        row=0, colspan=4, widgetkwargs={"foreground": self.theme_color})
        self.frame6.Seperator(col=0, row=1, colspan=4)
        self.denom_text = tkinter.Text(self.frame6.master, font=("Courier", int(self.screen_pad*0.23), "bold"),
                                       border=False)
        self.denom_text.tag_configure("center", justify='center')
        self.denom_text.grid(column=0, row=2, columnspan=4, rowspan=4, sticky="n", ipady=0)
        self.frame6.Button('❮', lambda: self.select_tab(1), col=4, rowspan=6, style='x.TButton')

        # Tab7 #
        self.frame7 = self.tab7.addFrame("Операционный день открыт")
        self.label7 = self.frame7.Label("Операционный день открыт", size=int(self.screen_pad * 0.8), col=0, row=0,
                                        colspan=4, pady=0, widgetkwargs={"foreground": self.theme_color,
                                                                         "justify": "center"})
        self.frame7.Seperator(col=0, row=1, colspan=4)
        self.denom_text1 = tkinter.Text(self.frame7.master, font=("Courier", int(self.screen_pad * 0.23), "bold"),
                                        border=False)
        self.denom_text1.tag_configure("center", justify='center')
        self.denom_text1.grid(column=0, row=2, columnspan=4, rowspan=4, ipady=0)
        self.frame7.Button('❮', lambda: self.select_tab(1), col=4, rowspan=6, style='x.TButton')

        # Tab8 #
        frame8 = self.tab8.addFrame("Откройте смену")
        frame_msg = frame8.addLabelFrame("", colspan=4)
        frame_msg.Label("Операционный день закрыт.\n Для начала работы откройте\n операционный день.",
                        size=int(self.screen_pad * 0.8), widgetkwargs={"foreground": self.theme_color,
                                                                       "justify": "center"})
        frame8.Button('❮', lambda: self.select_tab(0), col=4, style='x.TButton')

        # Tab9 #
        self.image = tkinter.PhotoImage(file="deep.png")
        self.deep_label = ttk.Label(self.tab9.master, image=self.image)
        self.deep_label.grid(row=0, column=0, columnspan=2)

        # Turn on power-board and init validator
        self.engine = Engine()
        self.engine.power_on_0ff(TURN_ON)
        self.port = self.engine.validator_init()
        # Start screensaver
        self.restart_screensaver()
        # Delay for better GUI display
        self.root.withdraw()
        self.root.after(500, self.show)

    def show(self):
        self.root.deiconify()

    def screensaver_start(self):
        if self.current_tab() == 0:
            self.select_tab(8)
            self.root.bind("<1>",  self.screensaver_finish)

    def screensaver_finish(self, event):
        self.select_tab(0)
        self.root.unbind("<1>")

    def restart_screensaver(self, event=None):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
        self.timer = self.root.after(150000, self.screensaver_start)

    def datetime_now(self, date_format):
        return datetime.now().strftime(date_format)

    def day_status_text(self, widget, denoms_dict, text):
        """Configure Close/Open bank day page Text widget"""
        widget.configure(state="normal")
        widget.delete("0.0", "end")
        widget.insert("end", f"{self.datetime_now('%Y-%m-%d %H.%M.%S')}\n{self.adres}В сумке:\n", "center")
        for denom, quantity in denoms_dict:
            widget.insert("end", f"{denom} руб. - {quantity} шт.\n", "center")
        widget.insert("end", f"\nИТОГО {str(self.data[0]['day_counter'])} руб.\n{text}", "center")
        widget.configure(state="disabled")

    def day_close(self):
        self.close_button.configure(state="disable")
        self.open_button.configure(state="normal")
        self.day_status = False
        self.data[0]["day_state"] = self.day_status
        self.json_write(self.data)
        self.day_status_text(self.denom_text, self.data[1].items(), "ОПЕРАЦИОННЫЙ ДЕНЬ\nЗАКРЫТ")
        text = self.denom_text.get("0.0", "end")
        print_receipt(text, receipt="close day", image=False)
        self.select_tab(5)

    def day_open(self):
        self.close_button.configure(state="normal")
        self.open_button.configure(state="disable")
        self.denom_dict = self.drop_dict(self.denom_dict)
        self.day_status = True
        self.receipt_number = 1
        self.data[0]["day_counter"] = 0
        self.data[0]["day_state"] = self.day_status
        self.data[0]["receipt_number"] = self.receipt_number
        self.data[1] = self.drop_dict(self.data[1])
        self.json_write(self.data)
        self.day_status_text(self.denom_text1, self.denom_dict.items(), "ОПЕР. ДЕНЬ ОТКРЫТ\nСЧЕТЧИКИ ОБНУЛЕНЫ")
        text = self.denom_text1.get("0.0", "end")
        print_receipt(text, receipt="open day", image=False)
        self.select_tab(6)

    def current_tab(self):
        return self.notebook.notebook.tabs().index(self.notebook.notebook.select())

    def select_tab(self, tab):
        self.notebook.notebook.select(tab)
        if tab == 0:
            self.restart_screensaver()  # restart timer of the screensaver
            self.edit_field = self.user_field
            self.user_field.focus_set()

    def tree_selection(self, event):
        item = self.tree.item(self.tree.selection())
        self.client = item["text"]
        self.account = item["values"][0]

    def update_counters(self):
        self.receipt_number += 1
        self.data[0]["day_counter"] += self.count
        self.data[0]["receipt_number"] = self.receipt_number
        for denom in self.data[1].keys():
            self.data[1][denom] += self.denom_dict[denom]
        self.json_write(self.data)
        self.denom_dict = self.drop_dict(self.denom_dict)
        self.count = 0

    def drop_dict(self, dct):
        return dct.fromkeys(("5", "10", "50", "100", "200", "500", "1000", "2000", "5000"), 0)

    def receipt_data(self):
        date = self.datetime_now("%d.%m.%Y\n%H:%M:%S")
        receipt_table = PrettyTable(["Дата/Время", "Сумма"], border=False)
        receipt_table.add_row([date, self.count])
        receipt_table.add_row(["\n" + self.dict_to_text(self.denom_dict)[0],
                               "\n" + self.dict_to_text(self.denom_dict)[1]])
        receipt_table.add_row(["ИТОГО", self.count])
        receipt_total = f"Чек № {self.receipt_number}\n{self.adres}{self.client}\n{self.account}\n\n{receipt_table}"
        qr_data = f"Чек № {self.receipt_number}\n{self.adres}{self.client}\n{self.account}\n{date}\nИТОГО {self.count}"
        make_qr(qr_data)
        return receipt_total

    def receipt_display(self, receipt_total):
        self.label_quantity.configure(text=self.dict_to_text(self.denom_dict)[1])
        self.label_deposit.configure(text=self.count)
        self.back_button.configure(state="normal")
        self.receipt_text.configure(text=receipt_total, font="Courier", justify="center")
        self.image_qr = tkinter.PhotoImage(file="tmpqr.png")
        self.qr_label.configure(image=self.image_qr)

    def receipt(self):
        receipt_data = self.receipt_data()
        self.receipt_display(receipt_data)
        self.update_counters()
        self.select_tab(4)
        print_receipt(receipt_data, "print_qr.png", str(self.receipt_number), image=True)

    def set_user_entry(self, event):
        self.edit_field = self.user_field

    def set_password_entry(self, event):
        self.edit_field = self.password_field

    def backspace(self):
        if self.del_flag:
            text = self.edit_field.get()
            self.edit_field.delete(len(text)-1)
            self.root.after(100,  self.backspace)

    def del_released(self, event):
        self.del_flag = False
        self.restart_screensaver()

    def del_pressed(self, event):
        self.del_flag = True
        self.backspace()

    def set_default_entry(self):
        self.user_field.delete(0, "end")
        self.password_field.delete(0, "end")

    def port_close(self):
        if self.port.is_open:
            self.port.close()

    def change_theme(self, theme, mode):
        self.port_close()
        self.data[2]["theme"] = theme
        self.data[2]["mode"] = mode
        self.json_write(self.data)
        self.handleExit()
        restart_program()

    def hide_pass(self):
        self.password_field.configure(show="✳")

    def show_pass(self):
        self.password_field.configure(show="")
        self.root.after(500, self.hide_pass)

    def verify_db_user(self, user, input_pass):
        user_dict = user.to_dict()
        if user_dict["status"] == "Кассир":
            password_hash = user_dict["password"]
            if pwd_context.verify(input_pass, password_hash):
                self.set_default_entry()
                if self.day_status:
                    for i in self.tree.get_children():
                        self.tree.delete(i)
                    for data in user.client:
                        tree_row = data.to_dict()
                        self.tree.insert('', 'end', text=tree_row["name"], values=tree_row["purpose"])
                    self.select_tab(3)
                    self.tree.selection_add(self.tree.get_children()[0])
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

    def authorization(self):
        input_user = self.user_field.get()
        input_pass = self.password_field.get()
        user = get_user(input_user)
        if user:
            self.verify_db_user(user, input_pass)
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
            self.root.after(100, lambda: self.engine.send_to_port(RESP_B5))
        elif input_user == "03" and input_pass == "03":
            self.port.close()
            self.handleExit()
        else:
            self.flashing()

    def flashing(self):
        self.flash("red")
        self.root.after(300, lambda: self.flash(self.theme_foreground))

    def flash(self, color):
        self.user_field.config(foreground=color)
        self.password_field.config(foreground=color)

    def digit_buttons(self, digit):
        if self.edit_field.get().isdigit() or self.edit_field.get() == "":
            self.edit_field.insert("end", digit)
        else:
            self.edit_field.delete("0", "end")
            self.edit_field.insert("end", digit)

    def json_read(self):
        with open("variables.json", "r", encoding="utf-8") as f:
            all_variables = load(f)
            return all_variables

    def json_write(self, data):
        with open("variables.json", "w", encoding="utf-8") as f:
            dump(data, f)

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
        self.state_butons_config("disable", "normal")
        try:
            self.select_tab(2)
            self.read_data_from_port()
        except Exception as e:
            self.engine.write_logs("a+", f"\n{e}")
            self.accept_button.configure(style="accept.TButton")
            self.root.after(300, lambda: self.accept_button.configure(style="TButton"))

    def start_count(self):
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

            if len_data:
                if event == b"48":  # Реакция на 48 событие ПОЛУЧЕН ОТЧЕТ ОБ ОШИБКЕ
                    self.port.write(RESP_48)
                if event == b"21":  # Реакция Hoper on событие
                    self.count_event_flag = True
                    self.start_count()
                    self.state_butons_config("disable", "disable")
                    self.port.write(RESP_HOP_ON)
                if event == b"22":  # Реакция Hoper off событие
                    self.port.write(RESP_HOP_OFF)
                    self.count_event_flag = False
                    if self.count != 0:
                        self.state_butons_config("normal", "disable")
                    else:
                        self.state_butons_config("disable", "normal")
                if event == b"28":  # Reaction to Banknotes don't Exist Reject event
                    self.port.write(RESP_REJ_OFF)
                if event == b"27":  # Reaction to Banknotes Exist on Reject event
                    self.port.write(RESP_REJ_ON)
                if event == b"41":  # Reaction to Send SC initialize Status & Result event ERROR RESET REPORT ACCEPTED
                    self.port.write(RESP_B5)
                if event == b"24":  # Reaction to Send Counting Result event (calculation data)
                    self.port.write(RESP_24)
                if event == b"45":  # Reaction to Deposit Ready Status event
                    self.port.write(RESP_45)

                if len_data == 64 and event == b"23" and error_hex == b"00":  # if count event and there is no error
                    self.count_event(denom_byte)
                if event == b"23" and chain_indicator == b'00' * 50:
                    self.engine.write_logs("a+", "Insert chain detected")

                if error_hex in REJECT_GROUP.keys() and reject_reason != b"0000" and event != b'24':
                    for error_text, error_code in RECO_ERROR.items():
                        if reject_reason == error_code:
                            self.engine.write_logs("a+", f"reject reason: {error_text}")

            threading_Timer(0.06, self.read_data_from_port).start()

    def count_event(self, denom_byte):
        nominal = unpack("<h", denom_byte)  # little-endian
        self.denom_dict[str(nominal[0])] += 1
        self.count += nominal[0]

        self.label_quantity.configure(text=self.dict_to_text(self.denom_dict)[1])
        self.label_deposit.configure(text=self.count)

    def enter_key(self, event):
        self.restart_screensaver()
        tab = self.current_tab()
        user = self.user_field.get()
        password = self.password_field.get()
        if tab == 0:
            if user and password:
                self.authorization()
            elif not password and user:
                self.edit_field = self.password_field
                self.password_field.focus_set()
            else:
                self.edit_field = self.user_field
                self.user_field.focus_set()
        if tab == 3:
            self.deposit_start()


if __name__ == '__main__':
    freeze_support()
    process = Process(target=loading)
    process.start()
    app = App()
    process.terminate()
    app.run(onlyFrames=False)
