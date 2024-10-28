from abc import ABC
from datetime import datetime

from view import View
from model import Animal

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
                    self.stack.append(AddAnimalController(self.view).start)
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


class AddAnimalController(Controller):

    def __init__(self, view: View = None):
        super().__init__(view)
        self.new_animal = Animal(None, None, list())
        self.stack.extend(
            [
                self.save_to_server,
                self.get_list_of_commands,
                self.get_date_of_birth,
                self.get_name
            ]
        )

    def get_name(self) -> None:
        intro = 'Введите имя животного:'
        self.new_animal.name = self.view.show_dialog(intro)

    def get_date_of_birth(self) -> None:
        intro = 'Введите дату рождения животного в формате дд.мм.гггг:'
        user_choice = self.view.show_dialog(intro)
        try:
            self.new_animal.date_of_birth = datetime.strptime(user_choice, '%d.%m.%Y').date()
        except ValueError:
            message = ('ОШИБКА ВВОДА:\n-> Пожалуйста, укажите дату рождения в формате дд.мм.гггг, где:\n'
                       '\t- дд - это день месяца с лидирующим нулём, например 01, 02...30, 31;\n'
                       '\t- мм - это месяц с лидирующим нулём, например 01, 02...11, 12;\n'
                       '\t- гггг - это год по грегорианскому календарю, например 1777, 1778...2023, 2024;\n'
                       '\t- "." - это разделитель частей даты рождения.')
            self.view.show_message(message)
            self.stack.append(self.get_date_of_birth)

    def get_list_of_commands(self) -> None:
        first_loop = not bool(self.new_animal.commands)
        if first_loop:
            intro: str = 'Животное обучено каким-то командам? Хотите внести их в карточку?'
        else:
            intro: str = 'Внести еще одну команду в карточку животного?'
        menu: list = ['Да', 'Нет']
        user_choice = self.view.show_menu(intro, menu)
        try:
            option = int(user_choice)
        except ValueError:
            message = 'ОШИБКА ВВОДА:\n-> Пожалуйста, укажите номер нужной опции.'
            self.view.show_message(message)
            self.stack.append(self.get_list_of_commands)
        else:
            match option:
                case 1:
                    self.add_new_command()
                    self.stack.append(self.get_list_of_commands)
                case 2:
                    pass
                case _:
                    message = ('ОШИБКА ВЫБОРА:\n-> Данный функционал еще не реализован, пожалуйста, '
                               'используйте другие функции.')
                    self.view.show_message(message)
                    self.stack.append(self.get_list_of_commands)

    def add_new_command(self) -> None:
        intro = ('Вводите по 1-й команде за раз, иначе данные будут искаженны, спасибо за понимание.\n'
                   'Укажите команду, которой обучено животное:')
        self.new_animal.commands.append(self.view.show_dialog(intro))

    def save_to_server(self):
        print(self.new_animal)