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
    def hash_password(password: str, login: str) -> str:
        """hash + salt"""
        salt = login + '123879yfhn34d02jd-923dfn8035h42-9h'
        return hashlib.sha512((password + salt).encode()).hexdigest()

class DataBase:
    __users = {
                'max': '86f81d401fdf767ac7faaedb4bf8e000e8efc1fe05faba05da1100bb8085be8f8acc4c08748de72c1420e1431851146f090626b9b2f5a35f9de092458f35a8c2', 
                'john': '643d0e177c787c7316aa88e4cc006454d979bd3e90f09d0e4eca20b69d7eb840eef774d8388c31c5bcd7099b6e02daf61771083b7dee0a40b78c7768a2764de3'
             }

    # ФУНКЦИИ ДЛЯ БЕЗОПАСНОЙ ПРОВЕРКИ БД
    def check_login(login: str) -> bool:
        is_correct = login in DataBase.__users.keys()
        return is_correct

    def check_password(login, input_psw) -> bool:
        '''secret compare with DB'''
        correct_psw = DataBase.__users.get(login)
        is_correct = secrets.compare_digest(input_psw, correct_psw)
        
        return is_correct

# Класс инициализации состояний авторизации
class AuthState(Enum):
    LOGIN = "Ввод логина"
    PASSWORD = "Ввод пароля"
    SUCCESS = "Доступ разрешен"
    FAILURE = "Доступ запрещен"
    INVALID_AUTH = "\nERROR: Неверный логин или пароль (Incorrect login or password)\n"
    RETRIES_ERROR = "\Слишком много попыток. Попробуйте позже"

    
class LoginSystem():
    
    RETRIES_ERROR = "\n[Слишком много попыток. Попробуйте позже]"
    counter_retries = 0
    MAX_RETRIES = 5
    def __init__(self) -> None: 
        
        self._state = AuthState.FAILURE

        self.login = None
        self.__password = None

    def input_login(self) -> None:        
        self._state = AuthState.LOGIN
        print(f"[SESSION STATE]: {self}")

        self.login = input("login: ")
        __log = DataBase.check_login(self.login)

        if __log:
            self._state = AuthState.PASSWORD
            self.input_password()
        else:
            self.retry_login()
        
    def input_password(self) -> None:
        print(f"[SESSION STATE]: {self}")

        # хэшируем
        self.__password = Hash.hash_password(self.login, getpass('password: '))
        
        # проверка в бд по хэшу
        psw = DataBase.check_password(self.login, self.__password)

        # если пароли совпадают
        if psw:
            self._state = AuthState.SUCCESS
            
        else:
            print(f"[SESSION STATE]: {self}")
            self.retry_login()
        
            
    def retry_login(self) -> str:
        LoginSystem.counter_retries += 1
        if LoginSystem.counter_retries == LoginSystem.MAX_RETRIES:
            print(LoginSystem.RETRIES_ERROR)
            time.sleep(5)
            LoginSystem.counter_retries = 0

        self._state = AuthState.INVALID_AUTH
        
        print(self)
        self.input_login()

    def __str__(self):
        return self._state.value


class UI:
    @staticmethod
    def show_start_title(user):
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
    def show_end_title(user):
        time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        print(
            f"\n├─SESSION STATE: {user}",
            f"├─{time}",
            "├─Вы вошли в систему",
            "---------------------------------------------------------------",
            sep='\n'
        )

    @staticmethod
    def show_desktop(user):
        # Рисуем рабочий стол
        COLORS = {
            "window": "\033[1;36m",
            "text": "\033[1;37m",
            "panel": "\033[48;5;234m\033[38;5;15m",
            "icon": "\033[1;32m",
            "reset": "\033[0m"
            }
        # Верхняя панель (системная)
        top_panel = f"{COLORS['panel']}           TempleOS  │  {datetime.now().strftime('%H:%M')} │  Wifi-Connected             {COLORS['reset']}"

        desktop = f"""
        {COLORS['window']}┌───────────────────────────────────────┐
        │{COLORS['text']}  {user}@TempleOS:~$ ./fsociety           {COLORS['window']}│
        │{COLORS['text']}  OS: TempleOS 6.6.0                   {COLORS['window']}│
        │{COLORS['text']}  Kernel: 6.6.0-Davis                  {COLORS['window']}│
        │{COLORS['text']}  Uptime: 0 days                       {COLORS['window']}│
        │{COLORS['text']}  Shell: /bin/bash                     {COLORS['window']}│
        │{COLORS['text']}  CPU: Intel Terry                     {COLORS['window']}│
        │{COLORS['text']}  Memory: 128M / 4096M                 {COLORS['window']}│
        └───────────────────────────────────────┘"""

        # Нижняя панель задач
        bottom_panel = f"{COLORS['panel']}        [💻] Терминал │ [📁] Документы │ [🌐] Браузер           {COLORS['reset']}"

        print(top_panel)
        print(desktop)
        print()
        print('\n[Добро пожаловать. Снова 🗲 ]')
        print(bottom_panel)

    @staticmethod
    def show_cancel_title():
        print("\n[SESSION CLOSED]")   


def main():
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