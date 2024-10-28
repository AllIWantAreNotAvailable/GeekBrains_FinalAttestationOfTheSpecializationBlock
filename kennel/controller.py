from abc import ABC
from datetime import datetime

from view import View

class Controller(ABC):

    def __init__(self, view: View = None):
        self.stack: list = list()
        self.view = view if view else View()

    def start(self):
        while self.stack:
            option = self.stack.pop()
            try:
                option()
            except KeyboardInterrupt:
                message = '\nОШИБКА ЗАВЕРШЕНИЯ ПРОЦЕССА:\n-> Для выхода из ПО укажите номер нужной опции.'
                self.view.show_message(message)
                self.stack.append(option)


class AppController(Controller):

    def __init__(self, view: View = None):
        super().__init__(view)
        self.greeting: bool = True
        self.stack.append(self.main_menu)


    def main_menu(self):
        intro: str = 'Пожалуйста, выберите функцию по её номеру:'
        if self.greeting:
            intro = 'Добро пожаловать в CRM-систему питомника животных!\n\n' + intro
            self.greeting = False
        menu: list = ['Добавить новое животное', 'Просмотреть всех животных в питомнике', 'Закрыть программу']
        user_choice = self.view.show_menu(intro, menu)
        try:
            option = int(user_choice)
        except ValueError:
            message = 'ОШИБКА ВВОДА:\n-> Пожалуйста, укажите номер нужной опции.'
            self.view.show_message(message)
            self.stack.append(self.main_menu)
        else:
            match option:
                case 1:
                    pass
                case 2:
                    pass
                case 3:
                    self.stack.clear()
                    message = 'До новых встреч!'
                    self.view.show_message(message)
                case _:
                    message = ('ОШИБКА ВЫБОРА:\n-> Данный функционал еще не реализован, пожалуйста, '
                               'используйте другие функции.')
                    self.view.show_message(message)
                    self.stack.append(self.main_menu)
