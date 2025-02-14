import tkinter as tk
from datetime import datetime
import tkinter.ttk as ttk
import tkinter.messagebox as mb


class App:
    def __init__(self):
        # Создаем главное окно приложения
        self.root = tk.Tk()
        self.root.title("Добавить клиента")
        self.root.protocol("WM_DELETE_WINDOW", self.handle_exit)
        self.root.iconbitmap(bitmap=None)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry(f"{width}x{height}+0+0")
        # self.root.attributes('-fullscreen', True)

        # self.screen_pad = self.root.winfo_screenwidth() * 0.05
        size = 13  # int(self.screen_pad * 0.18)

        font = ("Arial", size)
        self.style.configure('Treeview', font=font)
        self.style.configure('Treeview.Heading', font=("Arial", size, "bold"))
        self.style.map("Treeview", foreground=self.fixed_map("foreground"), background=self.fixed_map("background"))

        # Поле для ввода штрих-кода
        self.label_code = tk.Label(self.root, text="Введите штрих-код:", font=font)
        self.label_code.grid(row=0, column=0, sticky="e", padx=(10, 0))

        self.entry_code = tk.Entry(self.root, width=size*2, font=font)
        self.entry_code.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # Поле для суммы
        self.label_sum = tk.Label(self.root, text="Сумма:", font=font)
        self.label_sum.grid(row=1, column=0, sticky="e", padx=(10, 0))

        self.entry_sum = tk.Entry(self.root, width=size*2, font=font)
        self.entry_sum.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=size)

        # Кнопка для подтверждения и сохранения результата
        self.button_confirm = tk.Button(self.root, text="Внести в список", relief="groove",
                                        command=self.confirm_and_save, font=font, width=int(size*1.5),
                                        background="#dcdad5")
        self.button_confirm.grid(row=0, column=2, columnspan=1, pady=5)
        self.button_new_list = tk.Button(self.root, text="Новый список", relief="groove",
                                         command=self.new_count, font=font, width=int(size*1.5), background="#dcdad5")
        self.button_new_list.grid(row=0, column=3, pady=5)
        self.button_xml = tk.Button(self.root, text="Удалить БД", relief="groove",
                                    command=lambda: print("{{{{"), font=font, width=int(size*1.5),
                                    background="#dcdad5", state="disabled")
        self.button_xml.grid(row=1, column=3, columnspan=1)
        self.button_check = tk.Button(self.root, text="Сравнить", command=self.check_in_xml, font=font,
                                      width=int(size*1.5),
                                      background="#dcdad5", relief="groove")
        self.button_check.grid(row=1, columnspan=1, column=2)
        # Сообщение об ошибке или успешном сохранении
        self.message_label = tk.Label(self.root, text="", fg="black", font=font)
        self.message_label.grid(row=5, column=1, columnspan=4, sticky=tk.N + tk.S)

        # Список для отображения результатов
        columns = ("#1", "#2", "#3", "#4")# , "#5")
        self.tree = ttk.Treeview(show="headings", columns=columns)
        self.tree.heading("#1", text="Название")
        self.tree.heading("#2", text="Логин")
        self.tree.heading("#3", text="№ счета")
        self.tree.heading("#4", text="Адрес")
        # self.tree.heading("#5", text="Подробности просчета")
        self.tree["displaycolumns"] = columns
        self.tree.column("#1", width=int(width*0.15))
        self.tree.column("#2", width=int(width*0.15))
        self.tree.column("#3", width=int(width*0.33))
        self.tree.column("#4", width=int(width*0.33))

        ysb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ysb.set, height=25)
        self.tree.grid(row=4, column=0, columnspan=4, padx=15, sticky="snew")
        ysb.grid(row=4, column=0, columnspan=4, sticky=tk.N + tk.S + "e")
        self.tree.bind("<Double-1>", self.tree_selection)

        # Запускаем основной цикл приложения
        self.entry_code.focus_set()
        self.root.mainloop()

    def fixed_map(self, option):
        return [elm for elm in self.style.map("Treeview", query_opt=option)
                if elm[:2] != ("!disabled", "!selected")]

    def handle_exit(self):
    #     try:
    #         # delete_user_data()
    #         # delete_counter_data()
    #     except Exception as e:
    #         self.message_label.config(text=f"Ошибка БД или БД не найдена{e}", foreground="red")
        self.root.destroy()
        self.root.quit()

    def confirm_and_save(self):
        id_value = self.entry_code.get().strip()
        sum_value = self.entry_sum.get().strip()
        if id_value == "12345" and not sum_value:
            self.button_xml.configure(state="normal")
        else:
            status = "Не подтвержден"
            if not id_value.isdigit() or not sum_value.isdigit():
                self.message_label.config(text="Пожалуйста, заполните все поля цифрами!", fg="red")
                return

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_row = (current_time, id_value, sum_value, status)

            add_batch_data(id_value, sum_value, current_time, status)
            self.tree.insert("", tk.END, values=data_row)

            self.message_label.config(text=f"Сохранено: {data_row[0:-1]}", fg="green")

    def check_in_xml(self):
        open_file()
        change_status()
        self.message_label.configure(text="")
        self.tree.delete(*self.tree.get_children())
        for values in get_values_batch_db():
            if values[3] == 'ОК':
                self.tree.tag_configure("gr", foreground="green")
                self.tree.insert("", tk.END, values=values, tags=('gr',))
            else:
                self.tree.tag_configure("red", foreground="red")
                self.tree.insert("", tk.END, values=values, tags=("red",))

    def tree_selection(self, e):
        item = self.tree.item(self.tree.selection())
        count_info = item["values"][4]
        if count_info:
            msg = count_info[1:-1].replace("'", "").replace(",", "\n")
            mb.showinfo("Подробности просчета", msg)

    def new_count(self):
        delete_user_data()
        self.tree.delete(*self.tree.get_children())
        self.entry_sum.delete(0, "end")
        self.entry_code.delete(0, "end")
        self.entry_code.focus_set()
        self.message_label.config(text="")


if __name__ == "__main__":
    app = App()
