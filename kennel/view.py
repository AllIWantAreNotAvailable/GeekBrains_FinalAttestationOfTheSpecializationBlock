from jinja2 import Environment, PackageLoader, select_autoescape

ENV = Environment(
    loader=PackageLoader('kennel'),
    trim_blocks=True,
    lstrip_blocks=True,
    autoescape=select_autoescape()
)

class View:

    def __init__(self, env: Environment = ENV, prompt: str = '>>> '):
        self.env = env
        self.prompt = prompt

    def show_menu(self, list_intro: str, list_of_items: list[str]) -> str:
        template = self.env.get_template('list_smt.jinja')
        print(template.render(list_intro=list_intro, list_of_items=list_of_items))
        return input(self.prompt)

    def show_message(self, message: str) -> None:
        template = self.env.get_template('msg.jinja')
        print(template.render(message=message))

    def show_dialog(self, intro: str) -> str:
        template = self.env.get_template('add_smt.jinja')
        print(template.render(intro=intro))
        return input(self.prompt)
