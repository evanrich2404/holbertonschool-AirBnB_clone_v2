#!/usr/bin/python3
"""
The File storage module provides a way to store and retrieve data from a file
system. It defines a class that manages the storage of objects in JSON format
in a specified directory. It provides methods for adding, updating, and
deleting objects, as well as querying the stored data to retrieve objects based
on various criteria.
"""
import json
from models import base_model, user, state, city, amenity, place, review


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    MODLS = {
        'City': city.City,
        'State': state.State,
        'User': user.User,
        'Place': place.Place,
        'Amenity': amenity.Amenity,
        'Review': review.Review,
    }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            if cls in self.MODLS.keys():
                cls = self.MODLS.get(cls)
            nice_dict = {}
            for ky, vl in self.__objects.items():
                if cls == type(vl):
                    nice_dict[ky] = vl
            return nice_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """Delete obj From dictionary"""
        try:
            key = obj.__class__.__name__ + "." + obj.id
            del self.__objects[key]
        except (AttributeError, KeyError):
            pass

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """Deserialize JSON file to objects"""
        self.reload()
