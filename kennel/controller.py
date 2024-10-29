from view import View
from model import Model, MAIN_MENU


class NoSuchOptionException(IndexError):
    pass


class Controller:

    def __init__(self, view: View = None, model: Model = None):
        self.stack: list = [
            self._before_shutdown,
            self._before_startup
        ]
        self.view = view if view else View()
        self.model = model if model else Model()

    def _before_startup(self) -> None:
        self.view.show_template('message_greeting.jinja')

    def _before_shutdown(self) -> None:
        self.view.show_template('message_farewell.jinja')

    def start(self) -> None:
        while self.stack:
            try:
                self.stack[-1]()
            except KeyboardInterrupt:
                self.view.show_template('exception_keyboardInterrupt.jinja')
            except NoSuchOptionException:
                self.view.show_template('exception_noSuchOption.jinja')
            else:
                self.stack.pop()


class AppController(Controller):

    def __init__(self):
        super().__init__()
        self.stack.insert(-1, self.main_menu)

    def main_menu(self) -> None:
        std_in = self.view.show_dialog('menu.jinja', MAIN_MENU)
        try:
            option = int(std_in)
        except ValueError:
            self.view.show_template('exception_valueError.jinja')
        else:
            match option:
                case 0:
                    pass
                case 1:
                    pass
                case 2:
                    pass
                case _:
                    raise NoSuchOptionException
