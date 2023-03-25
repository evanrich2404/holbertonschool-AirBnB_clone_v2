#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")
if storage_type == "db":
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """A base class for all hbnb models"""
    if storage_type == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            kwargs = {}
        kwargs.setdefault('id', str(uuid4()))
        kwargs.setdefault('created_at', datetime.utcnow())
        if not isinstance(kwargs['created_at'], datetime):
            kwargs['created_at'] = datetime.strptime(
                kwargs['created_at'], '%Y-%m-%d %H:%M:%S.%f')
        kwargs.setdefault('updated_at', datetime.utcnow())
        if not isinstance(kwargs['updated_at'], datetime):
            kwargs['updated_at'] = datetime.strptime(
                kwargs['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
        if storage_type != "db":
            kwargs.pop('__class__', None)
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        cls_name = self.__class__.__name__
        dictionary = {
            k: v if type(v) == str else str(v)
            for k, v in self.__dict__.items()
        }
        dictionary.update({
            '__class__': cls_name,
        })
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
