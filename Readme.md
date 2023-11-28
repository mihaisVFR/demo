###  Программа для демонстрации KDS200 
Данная программа используется для демонстрации работы ADM KDS-200
Пользователи разделены на группы "Кассир" и "Инкассатор" и находятся
в базе данных `adm_demo.db`. Создание и работа с БД осуществлена
с помощью ORM sqlalchemy для добавления пользователей и клиентов можно использовать
функции `add_users` и `add_clients` из `model.py`.

Также использовался модуль тем tkinter `TKinterModernThemes`.
для корректной работы необходимо запускать GUI в полноэкранном режиме.
Для этого в файле `__init__.py` модуля `TKinterModernThemes` нужно изменить 
функцию `run` следующим образом:
        
        def run(self, cleanresize=True, recursiveResize=True, onlyFrames=True):
            if cleanresize:
                self.makeResizable(recursiveResize, onlyFrames=onlyFrames)
            self.root.update()
            self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
            self.root.attributes('-fullscreen', True)
            self.root.mainloop()


Так же для запуска необходимо:
Создать venv: `python3 -m venv <venv_name>`
Активировать venv: `source venv_name/bin/activate`
Установите зависимости: `pip install -r requirements.txt`
