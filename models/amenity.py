#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class Amenity(BaseModel, Base):
    """ Amenity class """
    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity")

    def __init__(self, *args, **kwargs):
        """ initializes amenity """
        if (os.getenv('HBNB_TYPE_STORAGE') != 'db'):
            self.name = ""
        super().__init__(*args, **kwargs)
