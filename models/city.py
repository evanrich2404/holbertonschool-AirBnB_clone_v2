#!/usr/bin/python3
""" Module that represents the City class """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    if storage_type == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        places = relationship("Place", backref="cities", cascade="all, delete")
    else:
        state_id = ""
        name = ""
        places = []
