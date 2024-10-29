from jinja2 import Environment, PackageLoader, select_autoescape, Template


class View:

    def __init__(self, prompt: str = '>>> '):
        self.env = Environment(
            loader=PackageLoader('kennel'),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=select_autoescape(enabled_extensions=('jinja', ))
        )
        self.prompt = prompt

    def _get_template(self, template_name: str) -> Template:
        return self.env.get_template(template_name)

    def _std_out(self, args, kwargs, template_name) -> None:
        template = self._get_template(template_name)
        print(template.render(*args, **kwargs))

    def _std_in(self) -> str:
        return input(self.prompt)

    def show_template(self, template_name: str, *args, **kwargs) -> None:
        self._std_out(args, kwargs, template_name)

    def show_dialog(self, template_name: str, *args, **kwargs) -> str:
        self._std_out(args, kwargs, template_name)
        return self._std_in()

