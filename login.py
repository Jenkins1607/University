# Задание: Реализация системы авторизации 
# с использованием конечного автомата
import time
from datetime import datetime
from enum import Enum
from getpass import getpass
import hashlib
import secrets
import sys

class Hash:
    def hash_password(login: str, password: str,) -> str:
        """hashing + salting"""
        salt = login + '123879yfhn34d02jd-923dfn8035h42-9h'
        return hashlib.sha512((password + salt).encode()).hexdigest()

class DataBase:
    __users = {
                'max': '1da2e1754bb45683edcb2e224a9460cda5ca9ae66f4769906f91d8cf27ab7c92671b27efb31422911201a9ec5621f1bb94d6d0304dae3c4e1d9e33085598b9d7', 
                'john': 'b9be7e37625503b2e793b27a1197a9f4fa53c770bb27accd2c7dbecb46f2b41fafca1a5a5b756524daf90ff8e78b9f6c655fdf95cf66ede767b17ab5af8b7687'
             }

    # ФУНКЦИИ ДЛЯ БЕЗОПАСНОЙ ПРОВЕРКИ БД
    def check_login(login: str) -> bool:
        return DataBase.__users.get(login) is not None
        

    def check_password(login: str, input_psw: str) -> bool:
        '''secret compare with DB'''
        correct_psw = DataBase.__users.get(login)
        return secrets.compare_digest(input_psw, correct_psw)

# Класс инициализации состояний авторизации
class AuthState(Enum):
    LOGIN = "Ввод логина"
    PASSWORD = "Ввод пароля"
    SUCCESS = "Доступ разрешен"
    FAILURE = "Доступ запрещен"
    INVALID_AUTH = "\nERROR: Неверный логин или пароль (Incorrect login or password)\n"

    
class LoginSystem():
    
    RETRIES_ERROR = "\n[Слишком много попыток. Попробуйте позже]"
    
    def __init__(self) -> None: 
        
        self._state = AuthState.FAILURE

        self.login = None
        self.__password = None

        self.BAN_LIMIT = 4
        self.MAX_RETRIES = 3
        self.retry_count = 0

    def input_login(self) -> None:        
        self._state = AuthState.LOGIN
        print(f"[SESSION STATE]: {self}")

        self.login = input("login: ")
        __log = DataBase.check_login(self.login)

        if __log:
            self._state = AuthState.PASSWORD
            self.input_password()
        else:
            print("[SESSION STATE]: Ввод пароля")
            fake_psw_input = input('password: ')

            self.retry_login()
        
    def input_password(self) -> None:
        print(f"[SESSION STATE]: {self}")

        # хэшируем
        self.__password = Hash.hash_password(self.login, getpass('password: '))
    
        # проверка на совпадение хэшей паролей
        psw = DataBase.check_password(self.login, self.__password)

        # если пароли совпадают
        if psw:
            self._state = AuthState.SUCCESS
            
        else:
            print(f"[SESSION STATE]: {self}")
            
            self.retry_login()
        
            
    def retry_login(self) -> None:
        self.retry_count += 1
        if self.retry_count >= self.BAN_LIMIT:
            print(UI.BAN_MESSAGE)
            sys.exit()

        if self.retry_count % self.MAX_RETRIES == 0:
            print(LoginSystem.RETRIES_ERROR)
            time.sleep(3)
        self._state = AuthState.INVALID_AUTH
        
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

    BAN_MESSAGE = """
            ⚡️💀 ВАС ЗАБАНИЛИ 💀⚡️

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Все попытки входа записаны
    • Ваш IP передан в 👮
    • Доступ уничтожен
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               ⚠️ Навсегда ⚠️
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
