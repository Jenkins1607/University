# Задание: Реализация системы авторизации 
# с использованием конечного автомата
import time
from datetime import datetime
from enum import Enum
from getpass import getpass
import hashlib
import secrets
import sys
import json

class DataBase:
    with open("users.json", "r") as db:
        _users = json.load(db)

# Класс инициализации состояний авторизации
class AuthState(Enum):
    LOGIN = "Ввод логина"
    PASSWORD = "Ввод пароля"
    SUCCESS = "Доступ разрешен"
    FAILURE = "Доступ запрещен"
    INVALID_AUTH = "\nERROR: Неверный логин или пароль (Incorrect login or password)\n"

class PasswordManager:
    def hash_password(login: str, password: str,) -> str:
        """hashing + salting"""
        salt = login + '123879yfhn34d02jd-923dfn8035h42-9h'
        return hashlib.sha512((password + salt).encode()).hexdigest()

    # ФУНКЦИИ ДЛЯ БЕЗОПАСНОЙ ПРОВЕРКИ БД
    def check_password(login: str, input_psw: str) -> bool:
        '''secret compare with DB'''
        correct_psw = DataBase._users.get(login)
        return secrets.compare_digest(input_psw, correct_psw)

    def check_login(login: str) -> bool:
        return DataBase._users.get(login) is not None

class DefenceManager:
    RETRIES_ERROR = "\n[Слишком много попыток. Попробуйте позже]"
    def __init__(self):
        self.BAN_LIMIT = 4
        self.MAX_RETRIES = 3
        self.retry_count = 0

    def check_retries(self):
        self.retry_count += 1
        if self.retry_count >= self.BAN_LIMIT:
            print(UI.BAN_MESSAGE)
            sys.exit()

        if self.retry_count % self.MAX_RETRIES == 0:
            print(DefenceManager.RETRIES_ERROR)
            time.sleep(3)
        
class LoginSystem():
    def __init__(self) -> None: 
        
        self._state = AuthState.FAILURE

        self.login = None
        self.__password = None

        self.BAN_LIMIT = 4
        self.MAX_RETRIES = 3
        self.retry_count = 0

    def input_login(self) -> None:        
        self._state = AuthState.LOGIN
        UI.show_state(self)

        self.login = input("login: ")
        __log = PasswordManager.check_login(self.login)

        if __log:
            self._state = AuthState.PASSWORD
            self.input_password()
        else:
            print("[SESSION STATE]: Ввод пароля")
            fake_psw_input = getpass('password: ')

            self.retry_login()
        
    def input_password(self) -> None:
        UI.show_state(self)

        # хэшируем
        self.__password = PasswordManager.hash_password(self.login, getpass('password: '))
    
        # проверка на совпадение хэшей паролей
        psw = PasswordManager.check_password(self.login, self.__password)

        # если пароли совпадают
        if psw:
            self._state = AuthState.SUCCESS
            
        else:
            UI.show_state(self)
            self.retry_login()
        
            
    def retry_login(self) -> None:
        self.defence = DefenceManager()
        self._state = AuthState.INVALID_AUTH
        
        DefenceManager.check_retries(self)
        print(self)
        self.input_login()

    def __str__(self) -> str:
        return self._state.value


class UI:
    @staticmethod
    def show_start_title(user: str) -> None:
        time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        print(
            "---------------------------------------------------------------",
            "├─АUTH SESSION",
            "├─INFO: Use (ctrl+c) if you want close the auth programm",
            f"├─SESSION STATE: {user}",
            f"├─{time}\n",
            sep='\n'
        )

    @staticmethod
    def show_end_title(user: str) -> None:
        time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        print(
            f"\n├─SESSION STATE: {user}",
            f"├─{time}",
            "├─Вы вошли в систему",
            "---------------------------------------------------------------",
            sep='\n'
        )

    @staticmethod
    def show_state(user):
        print(f"[SESSION STATE]: {user}")

    @staticmethod
    def show_desktop(user: str) -> None:
        # Рисуем рабочий стол
        COLORS = {
            "window": "\033[1;36m",
            "text": "\033[1;37m",
            "panel": "\033[48;5;234m\033[38;5;15m",
            "icon": "\033[1;32m",
            "reset": "\033[0m"
            }
        # Верхняя панель (системная)
        top_panel = f"{COLORS['panel']}         kali linux  │  {datetime.now().strftime('%H:%M')} │  Wifi-Connected             {COLORS['reset']}"

        desktop = f"""
        {COLORS['window']}┌───────────────────────────────────────┐
        │{COLORS['text']}  {user}@kali:~$ ./fsociety               {COLORS['window']}│
        │{COLORS['text']}  OS: kali 6.6.0                       {COLORS['window']}│
        │{COLORS['text']}  Kernel: 6.6.0-Davis                  {COLORS['window']}│
        │{COLORS['text']}  Uptime: 0 days                       {COLORS['window']}│
        │{COLORS['text']}  Shell: /bin/bash                     {COLORS['window']}│
        │{COLORS['text']}  CPU: Intel Terry                     {COLORS['window']}│
        │{COLORS['text']}  Memory: 128M / 8192M                 {COLORS['window']}│
        └───────────────────────────────────────┘"""

        # Нижняя панель задач
        bottom_panel = f"{COLORS['panel']}        [💻] Терминал │ [📁] Документы │ [🌐] Браузер           {COLORS['reset']}"

        print(top_panel)
        print(desktop)
        print()
        print('\n               [Добро пожаловать. Снова 🗲 ]')
        print(bottom_panel)

    @staticmethod
    def show_cancel_title() -> None:
        print("\n[SESSION CLOSED]")   

    # BAN_MESSAGE = """
    #         ⚡️💀 ВАС ЗАБАНИЛИ 💀⚡️

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # • Все попытки входа записаны
    # • Ваш IP передан в 👮
    # • Доступ уничтожен
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    #            ⚠️ Навсегда ⚠️
    # """
    BAN_MESSAGE = """
██████╗  █████╗ ███╗   ██╗    ███████╗██████╗ ██╗   ██╗██╗███╗   ██╗███████╗
██╔══██╗██╔══██╗████╗  ██║    ██╔════╝██╔══██╗██║   ██║██║████╗  ██║██╔════╝
██████╔╝███████║██╔██╗ ██║    █████╗  ██████╔╝██║   ██║██║██╔██╗ ██║█████╗  
██╔══██╗██╔══██║██║╚██╗██║    ██╔══╝  ██╔══██╗╚██╗ ██╔╝██║██║╚██╗██║██╔══╝  
██████╔╝██║  ██║██║ ╚████║    ███████╗██║  ██║ ╚████╔╝ ██║██║ ╚████║███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚═╝  ╚═══╝╚══════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ТВОЙ IP УЖЕ В БАЗЕ ОРГОВ И НА КАЖДОЙ ВОЛЧАТКЕ
• ВСЕ ТВОИ ДАННЫЕ ПРОДАНЫ НА ЧЁРНОМ РЫНКЕ
• ТВОЙ ЖЁСТКИЙ ДИСК СЕЙЧАС ПЫТАЮТ В ШИЗО
• ТВОИ СОЦСЕТИ СТАЛИ ДОНОСНЫМИ БЛОКНОТАМИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           🔒 ТЕПЕРЬ ТЫ - БЫДЛОКОД 🔒
           ☠ НИ ПАРАШИ НА ВОЛЮ ☠
"""

def main() -> None:
    try:
        user = LoginSystem()        
        UI.show_start_title(user)
        user.input_login()
        UI.show_end_title(user)
        UI.show_desktop(user.login)
    except KeyboardInterrupt:
        print()
        UI.show_cancel_title()
        sys.exit()
        
        
main()