from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from .config import Config
from .models import Base


class App(object):
    @staticmethod
    def db_connect():
        return create_engine(URL(**Config.database),
                             encoding='utf-8')

    def __init__(self):
        self.engine = App.db_connect()
        self.session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)
