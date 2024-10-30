from abc import ABC

from typing import Callable, Never
from enum import Enum

from view import View
from model import Model
from exception import NoSuchOptionError


class Signals(Enum):
    EXIT = -1
    DONE = 0
    ERROR = 1


class AbcController(ABC):

    def __init__(self, stack: list[Callable[[], Signals]] = None, view: View = None, model: Model = None) -> None:
        self.view = view if view else View()
        self.model = model if model else Model()
        self.stack = stack if stack else list()

    @staticmethod
    def __assertion_error(message: str) -> Never:
        assert True, message

    def __catcher(self, func: Callable[[], Signals]) -> Signals:
        signal: Signals = Signals.ERROR
        try:
            signal = func()
        except KeyboardInterrupt:
            self.view.show_template('exception_keyboardInterrupt.jinja')
        except ValueError:
            self.view.show_template('exception_valueError.jinja')
        except NoSuchOptionError:
            self.view.show_template('exception_noSuchOptionError.jinja')
        except Exception:
            self.view.show_template(str(Exception)) # TODO Check traceback stdout from view with jinja
        return signal

    def _loop(self) -> None:
        while self.stack:
            length = len(self.stack)
            func = self.stack.pop()
            signal: Signals = self.__catcher(func)
            match signal:
                case Signals.EXIT:
                    pass
                case Signals.DONE:
                    pass
                case Signals.ERROR:
                    if not length < len(self.stack):
                        self.stack.pop()
                    self.stack.append(func)
                case _:
                    self.__assertion_error('Paranoia')

    def choices(self, option: int) -> Signals:
        pass

    def start(self) -> None:
        pass


class Controller(AbcController):

    def __init__(self, stack: list[Callable[[], Signals]] = None, view: View = None, model: Model = None) -> None:
        super().__init__(stack, view, model)

    def start(self) -> None:
        self.stack.append(self.before_shutdown)
        AppController(self.stack).start()
        self.stack.append(self.before_startup)
        super()._loop()

    def before_startup(self) -> Signals:
        self.view.show_template('message_greeting.jinja')
        return Signals.DONE

    def before_shutdown(self) -> Signals:
        self.view.show_template('message_farewell.jinja')
        return Signals.DONE


class AppController(AbcController):

    def __init__(self, stack: list[Callable[[], Signals]] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stack = stack if stack else list()

    def choices(self, option: int) -> Signals:
        match option:
            case 0:
                return Signals.EXIT
            case 1:
                NewAnimalController(self.stack).start()
            case 2:
                pass
            case _:
                raise NoSuchOptionError
        return Signals.DONE

    def start(self) -> None:
        self.stack.append(self.main_menu)

    def main_menu(self) -> Signals:
        std_in = self.view.show_dialog('menu_main.jinja')
        return self.choices(int(std_in))


class NewAnimalController(AbcController):

    def __init__(self, stack: list[Callable[[], Signals]] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.stack = stack if stack else list()

    def choices(self, option: int) -> Signals:
        match option:
            case 0:
                AppController(self.stack).start()
                return Signals.EXIT
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case _:
                raise NoSuchOptionError
        return Signals.DONE

    def start(self) -> None:
        self.stack.append(self.add_new_animal_menu)

    def add_new_animal_menu(self) -> Signals:
        std_in = self.view.show_dialog('menu_add_new_animal.jinja')
        return self.choices(int(std_in))
