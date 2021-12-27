import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from libs import settings

DATABASES = settings.DATABASES

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    app_name = 'default'

    @classmethod
    def session(cls):
        return cls.get_db_session()

    @classmethod
    def objects(cls):
        return cls.get_db_session().query(cls)

    @classmethod
    def get_db_session(cls):
        engine = create_engine(settings.convert_db_conf_to_url(DATABASES.get(cls.app_name)))
        return sessionmaker(bind=engine)()

    @classmethod
    def get_conn(cls):
        db_config = DATABASES[cls.app_name]
        return pymysql.connect(
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            database=db_config['NAME'],
            port=db_config['PORT'],
        )

    def to_json(self, *args):
        dict_ = self.__dict__
        dict_.pop("_sa_instance_state", None)
        if not args:
            return dict_
        res = {}
        for item in args:
            res[item] = dict_[item]
        return res

    def to_tuple(self, *args):
        dict_ = self.__dict__
        dict_.pop("_sa_instance_state", None)
        if not args:
            return tuple(dict_.values())
        res = []
        for item in args:
            res.append(dict_[item])
        return tuple(res)
