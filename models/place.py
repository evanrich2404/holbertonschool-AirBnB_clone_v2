#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from os import getenv
from models.review import Review
from sqlalchemy.orm import relationship
storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))



class Place(BaseModel, Base):
        """ A place to stay """
        if storage_type == "db":
            __tablename__ = "places"
            city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
            user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
            name = Column(String(128), nullable=False)
            description = Column(String(1024), nullable=True)
            number_rooms = Column(Integer, nullable=False, default=0)
            number_bathrooms = Column(Integer, nullable=False, default=0)
            max_guest = Column(Integer, nullable=False, default=0)
            price_by_night = Column(Integer, nullable=False, default=0)
            latitude = Column(Float, nullable=True)
            longitude = Column(Float, nullable=True)
            amenity_ids = []
            reviews = relationship(
                "Review", backref="place", cascade="all, delete")
            amenities = relationship(
                "Amenity", secondary=place_amenity, viewonly=False)

        else:
            city_id = ""
            user_id = ""
            name = ""
            description = ""
            number_rooms = 0
            number_bathrooms = 0
            max_guest = 0
            price_by_night = 0
            latitude = 0.0
            longitude = 0.0
            amenity_ids = []

            @property
            def reviews(self):
                """getter for reviews """
                from models import storage
                reviews = []
                for x in storage.all(Review).values():
                    if x.place_id == self.id:
                        reviews.append(x)
                return reviews

            @property
            def amenities(self):
                """getter for amenities """
                from models import storage
                from models.amenity import Amenity
                amenity = []
                amensto = storage.all(Amenity)
                
                for x in amensto.values():
                    if x.id in self.amenity_ids:
                        amenity.append(x)
                return amenity

            @amenities.setter
            def amenities(self, amenity_list):
                """setter for amenities """
                from models.amenity import Amenity
                for x in amenity_list:
                    if type(x) == Amenity:
                        self.amenity_ids.append(x)

            @reviews.setter
            def reviews(self, review_object):
                if review_object and review_object not in self.review_ids:
                    self.review_ids.append(review_object)
