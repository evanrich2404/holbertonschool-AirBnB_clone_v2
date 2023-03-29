#!/usr/bin/python3
"""This module defines a class BaseModel to be used by all the other classes
in the project."""
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
    """This is the base model class for all other classes in the project.
    It includes common attributes and methods for all models to inherit."""
    if storage_type == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of the BaseModel class.

        Args:
            id (str): A UUID unique identifier for the instance.
            created_at (datetime): The datetime when the instance was created.
            updated_at (datetime): The datetime when the instance was updated.
        """
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
        """Update the updated_at attribute with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
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
