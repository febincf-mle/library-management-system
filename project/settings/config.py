import os


class BaseConfig:
    DEBUG=False
    SECRET_KEY="2RR894H8GFH03HHT430R04RJJ0"


class DevelopmentConfig(BaseConfig):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), '../library_db.sqlite3'))
    JWT_SECRET_KEY='94RU94UR84848H84HR84H8RH48R8H48R84H'
    broker_url='redis://127.0.0.1:6379/0'
    result_backend ='redis://127.0.0.1:6379/0'


class ProductionConfig(BaseConfig):
    pass