from sqlalchemy import create_engine

__DEFAULT_MENU_INTRO = 'Выберите номер нужного пункта меню'
MAIN_MENU = dict(
    title='ГЛАВНОЕ МЕНЮ',
    intro=__DEFAULT_MENU_INTRO,
    options=[
        'Добавить новое животное в реестр',
        'Просмотреть всех животных в реестре'
    ]
)


class Model:

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)