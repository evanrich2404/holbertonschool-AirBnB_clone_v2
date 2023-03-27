#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
storage_type = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    if storage_type == "db":
        from models.place import place_amenity
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenity = relationship("Place", secondary=place_amenity)
    else:
        name = ""
