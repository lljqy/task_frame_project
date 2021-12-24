from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from libs import settings

DATABASES = settings.DATABASES

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    app_name = None

    @classmethod
    def session(cls):
        return cls.get_db_session()

    @classmethod
    def objects(cls):
        return cls.get_db_session().query(cls)

    @classmethod
    def get_db_session(cls):
        if cls.app_name is None:
            raise NotImplementedError('子类模型必须指定`app_name`')
        engine = create_engine(DATABASES.get(cls.app_name))
        return sessionmaker(bind=engine)()

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
