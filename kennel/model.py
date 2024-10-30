from sqlalchemy import create_engine


class Model:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Model, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)