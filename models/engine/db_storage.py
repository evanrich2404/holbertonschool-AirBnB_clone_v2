#!/usr/bin/python3
"""This module defines a class to manage sql storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models import state, city, amenity, place, review, user


class DBStorage:
    __engine = None
    __session = None
    MODLS = {
        'City': city.City,
        'State': state.State,
        'User': user.User,
        'Place': place.Place,
        'Amenity': amenity.Amenity,
        'Review': review.Review,
    }

    def __init__(self):
        """init engine"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.
            format(getenv('HBNB_MYSQL_USER'),
                   getenv('HBNB_MYSQL_PWD'),
                   getenv('HBNB_MYSQL_HOST'),
                   getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)

    def all(self, cls=None):
        """query on the database"""
        object_dict = {}
        query = []
        if cls is None:
            for cls_type in DBStorage.MODLS.values():
                query.extend(self.__session.query(cls_type).all())
        else:
            if cls in self.MODLS.keys():
                cls = self.MODLS.get(cls)
            query = self.__session.query(cls)
        for obj in query:
            object_key = "{}.{}".format(type(obj).__name__, obj.id)
            object_dict[object_key] = obj
        return object_dict

    def gettables(self):
        inspector = inspect(self.__engine)
        return inspector.get_table_names()

    def meta(self, cls):
        metadata = MetaData()
        metadata.reflect(bind=self.__engine)
        table = metadata.tables.get(cls.__tablename__)
        self.__session.execute(table.delete())
        self.save()

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
        Base.metadata.create_all(self.__engine)
        session_temp = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_temp)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()
