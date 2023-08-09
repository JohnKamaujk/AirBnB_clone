#!usr/bin/python3
"""Defines the BaseModel class"""

import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """Represents the Base class of the project."""

    def __init__(self, *args, **kwargs):
        """Initialize a BaseModel instance.

        Args:
            *args (any): Unused.
            **kwargs (dict): key/value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        time_format = "%Y-%m-%dT%H:%M:%S.%f"

        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, time_format)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def __str__(self):
        """Return string representation of BaseModel instance."""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)

    def save(self):
        """Updates attribute updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Return the dictionary of the BaseModel instance.

        Includes the key/value pair __class__ representing
        the class name of the object.
        """
        dictionary = self.__dict__.copy()
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        dictionary["__class__"] = self.__class__.__name__
        return dictionary
