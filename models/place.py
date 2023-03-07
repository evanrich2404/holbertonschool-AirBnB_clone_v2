#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
import os


place_amenity = Table('place_amenity',
                    Base.metadata,
                    Column(
                        'place_id', String(60), ForeignKey('places.id'),
                        primary_key=True, nullable=False),
                    Column('amenity_id', String(60), ForeignKey('amenities.id'),
                        primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
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

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        from sqlalchemy.orm import relationship
        reviews = relationship(
            "Review", backref="place", cascade="all, delete")
    else:
        @property
        def reviews(self):
            """getter for reviews """
            from models import storage
            from models.review import Review
            reviews = []
            for key, value in storage.all(Review).items():
                if value.place_id == self.id:
                    reviews.append(value)
            return reviews

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False)
    else:
        @property
        def amenities(self):
            """getter for amenities """
            from models import storage
            from models.amenity import Amenity
            amenities = []
            for key, value in storage.all(Amenity).items():
                if value.id in self.amenity_ids:
                    amenities.append(value)
            return amenities

        @amenities.setter
        def amenities(self, obj):
            """setter for amenities """
            if type(obj).__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
