###  Программа для демонстрации KDS200 
Данная программа используется для демонстрации работы ADM KDS-200
Пользователи разделены на группы "Кассир" и "Инкассатор" и находятся
в базе данных `adm_demo.db`. Создание и работа с БД осуществлена
с помощью ORM sqlalchemy, для добавления пользователей и клиентов можно использовать
функции `add_users` и `add_clients` из `model.py`.
Так же прописаны следующие "служебные" комбинации:

        | Логин | Пароль | Описание                     |
        |-------|--------|------------------------------|
        | 3     | 3      | сменить на тему оформления 2 |
        | 4     | 4      | сменить на тему оформления 3 |
        | 5     | 5      | сменить на тему оформления 4 |
        | 6     | 6      | сменить на тему оформления 1 |
        | 31    | 31     | Отключить питание валидатора |
        | 32    | 32     | Включить питание валидатора  |
        | 55    | 55     | Сброс ошибки валидатора      |
        | 03    | 03     | Выйти из программы           |

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

Полезное:
Создать исполняемый файл windows используя nuitka:
1. в файле __init__.py модуля TKinterModernThemes строки 64 и 65 на:
theme_path = os.path.abspath(os.path.join(__file__ ,"..\\themes"))
path = os.path.abspath(theme_path +"\\"+ theme.lower() + "\\" + theme.lower() + ".tcl")
чтобы избежать исключения tcl после сборки (invalid command "set_theme")
2. в директорию программы должен быть путь к tcl файлам модуля TKinterModernThemes
__file__\TKinterModernThemes\themes
3. запустить сборку командой
`python -m nuitka --standalone --follow-imports 
--windows-icon-from-ico=adm.ico --disable-console 
--enable-plugin=tk-inter --include-module=TKinterModernThemes adm_demo.py` 
