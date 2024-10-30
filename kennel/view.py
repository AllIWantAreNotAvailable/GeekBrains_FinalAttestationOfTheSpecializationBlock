from jinja2 import Environment, PackageLoader, select_autoescape, Template


class View:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(View, cls).__new__(cls)

        return cls.__instance

    def __init__(self, prompt: str = '>>> ') -> None:
        self.env = Environment(
            loader=PackageLoader('kennel'),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(enabled_extensions=('jinja', ))
        )
        self.prompt = prompt

    def _get_template(self, template_name: str) -> Template:
        return self.env.get_template(template_name)

    def _std_out(self, template_name, *args, **kwargs) -> None:
        template = self._get_template(template_name)
        print(template.render(*args, **kwargs))

    def _std_in(self) -> str:
        return input(self.prompt)

    def show_template(self, template_name: str, *args, **kwargs) -> None:
        self._std_out(template_name, *args, **kwargs)

    def show_dialog(self, template_name: str, *args, **kwargs) -> str:
        self.show_template(template_name, *args, **kwargs)
        return self._std_in()

