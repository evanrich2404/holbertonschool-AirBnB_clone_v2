#!/usr/bin/python3
"""This module defines a class to manage sql storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from models.base_model import Base
import os


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """init engine"""
        data = []
        data[0] = os.getenv("HBNB_MYSQL_USER")
        data[1] = os.getenv('HBNB_MYSQL_PWD')
        data[2] = os.getenv('HBNB_MYSQL_HOST') or 'localhost'
        data[3] = os.getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            "mysql+mysqldb://{0}:{1}@{2}/{3}"
            .format(data[0], data[1], data[2], data[3]),
            pool_pre_ping=True)
        self.reload()
        if (os.getenv('HBNB_ENV') == 'test'):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the database"""
        if cls is None:
            return self.__session.query(Base).all()
        else:
            return self.__session.query(cls).all()

    def new(self, obj):
        """add the object to the database"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(bind=self.__engine)(
                expire_on_commit=False, scoped_session=False)
