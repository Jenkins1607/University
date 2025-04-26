import sys
from datetime import datetime
from enum import Enum
import hashlib
import secrets
import json
from getpass import getpass

class Hash:
    def hash_password(login: str, password: str) -> str:
        salt = login + '123879yfhn34d02jd-923dfn8035h42-9h'
        return hashlib.sha512((password + salt).encode()).hexdigest()

class DataBase:

    with open("users.json", "r") as db:
        __users = json.load(db)
        print(type(__users))        

    # ФУНКЦИИ ДЛЯ БЕЗОПАСНОЙ ПРОВЕРКИ БД
    def check_login(login: str) -> bool: 
        return login in DataBase.__users

    def check_password(login: str, input_psw: str) -> bool:
        correct_psw = DataBase.__users.get(login)
        is_correct = secrets.compare_digest(input_psw, correct_psw)
        
        return is_correct
    
    # функция для регистрации

    def reg(login,hashed_psw):
        DataBase.__users[login] = hashed_psw
        with open("users.json", 'w') as db:
            json.dump(DataBase.__users, db, indent=2)
        


class RegState(Enum):
    LOGIN = "Ввод логина"
    PASSWORD = "Ввод пароля"
    SUCCESS = "Вы успешно зарегистрированы"


class Reg:
    LENGTH = 10
    # ошибки
    error_psw = "\n[INFO] Password is invalid, try again"    
    error_log = "\n[INFO] Login is already exist"
    success_message = "\nSuccessful registration!"
    not_matching_passwords ="\npassword is not matching, try again"

    def __init__(self) -> None:        
        self._state = RegState.LOGIN
        self.__password = None
        self.__login = None

    def input_password(self):
        self._state = RegState.PASSWORD
        print(f"\nSESSION STATE: {self}")
        while True:
            password_1 = input("Password: ")
            password_2 = input("Enter your password again: ")

            match = password_1 == password_2
            if match:
                self.__password = password_1
                break
            else:
                print(Reg.not_matching_passwords)
                
        self.validation_psw()

    def input_login(self):
        print(f"SESSION STATE: {self}")
        while True:
            self.__login = input("Login: ")
            has_login = DataBase.check_login(self.__login)

            if not has_login:
                break
            else:
                print(Reg.error_log)
                print(f"SESSION STATE: {self}")
        self.input_password()


    def validation_psw(self):
        if len(self.__password) < Reg.LENGTH:
            print(Reg.error_psw)
            self.input_password()
        else:
            is_alnum = self.__password.isalnum()
            if is_alnum:
                has_upper = any(chr.isupper() for chr in self.__password)
                has_lower = any(chr.islower() for chr in self.__password)

                if has_upper and has_lower:
                    self.register(self.__login, self.__password)
                    return True
                
            print(f"SESSION STATE: {self}")
            self.input_password()


    def register(self, login, psw):
        hashed_psw = Hash.hash_password(login, psw)
        DataBase.reg(self.__login, hashed_psw)
        print(Reg.success_message)
        

    def __str__(self):
       return self._state.value

# Класс инициализации состояний авторизации
class AuthState(Enum):
    LOGIN = "Ввод логина"
    PASSWORD = "Ввод пароля"
    SUCCESS = "Доступ разрешен"
    FAILURE = "Доступ запрещен"

class LoginSystem():
    
    INVALID_AUTH = "\nERROR: Неверный логин или пароль (Incorrect login or password)\n"
    
    def __init__(self) -> None: 
        
        self._state = AuthState.FAILURE

        self.__login = None
        self.__password = None

    def auth_input(self):
        auth = None

        while True:
            self._state = RegState.LOGIN
            print(f"SESSION STATE: {self}")
            self.__login = input("login: ")

            self._state = RegState.PASSWORD
            print(f"\nSESSION STATE: {self}")
            self.__password = Hash.hash_password(self.__login, getpass("password: "))
            
            has_login = DataBase.check_login(self.__login)

            if has_login:
                
                has_psw = DataBase.check_password(self.__login, self.__password)
                
                if has_psw:
                    self._state = RegState.SUCCESS
                    break

            print(LoginSystem.INVALID_AUTH)

    def __str__(self):
       return self._state.value
    


class UI:
    @staticmethod
    def show_start_menu():
        time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        print(
            "---------------------------------------------------------------",
            "├─АUTH SESSION",
            "├─INFO: Use (ctrl+c) to close the auth program",
           f"├─{time}",
           sep='\n'
        
        )
    @staticmethod
    def show_options():
        print("\nВыберите опцию:")
        print("1. Войти")
        print("2. Регистрация")


    @staticmethod
    def show_end_session(auth_obj):
        time = datetime.today().strftime("%d.%m.%Y %H:%M:%S")
        print(
            f"\n├─SESSION STATE: {auth_obj}",
            f"├─{time}",
            "├─Вы вошли в систему",
            "---------------------------------------------------------------",
            sep='\n'
        )

    @staticmethod
    def show_cancel_title():
        print("\n[SESSION CLOSED]")   

    @staticmethod
    def show_desktop():
        # Рисуем рабочий стол
        COLORS = {
            "window": "\033[1;36m",
            "text": "\033[1;37m", 
            "icon": "\033[1;32m"
            }

        desktop = f"""
        {COLORS['window']}┌───────────────────────────────────────┐
        │{COLORS['text']}  user@penguin:~$ neofetch             {COLORS['window']}│
        │{COLORS['text']}  OS: TuxOS 6.6.0                      {COLORS['window']}│
        │{COLORS['text']}  Kernel: 6.6.0-penguin                {COLORS['window']}│
        │{COLORS['text']}  Uptime: 0 days                       {COLORS['window']}│
        │{COLORS['text']}  Shell: /bin/bash                     {COLORS['window']}│
        │{COLORS['text']}  CPU: Intel Penguin                   {COLORS['window']}│
        │{COLORS['text']}  Memory: 128M / 4096M                 {COLORS['window']}│
        └───────────────────────────────────────┘"""

        icons ="        [📁] Документы  [💻] Терминал  [🌐] Браузер "

        print(desktop,  icons, sep='\n')
        print()

def main():
    UI.show_start_menu()
    UI.show_options()
    user = LoginSystem()
    reg = Reg()

    while True:
        try:
            print()
            choice = input("Опция: ")
            print()
            if choice == "1":
                user.auth_input()
                UI.show_end_session(user)
                print()
                UI.show_desktop()
                print('\nДобро пожаловать. Снова.')
                break

            elif choice == "2":
                reg.input_login()
                UI.show_start_menu()
                user.auth_input()
                UI.show_end_session(user)
                UI.show_desktop()
                break

            else:
                print("[ERROR]: Incorrect choice\n")
                continue
        except KeyboardInterrupt:
            UI.show_cancel_title()
            sys.exit()



if __name__ == "__main__":
    main()
