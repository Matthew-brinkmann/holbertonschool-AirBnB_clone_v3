#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

from models.expections import *

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

    @classmethod
    def storage_update(cls, listToIgnore, resuestDataAsDict, ObjToUpdate):
        """handles the update command for all types
        Return Values: 0: Success
        Exceptions Raised
        -1: BaseModelInvalidObject
        -2: BaseModelInvalidJson"""
        if not cls.test_request_data(resuestDataAsDict):
            raise BaseModelInvalidDataDictionary(resuestDataAsDict)
        if ObjToUpdate is None:
            raise BaseModelInvalidObject(ObjToUpdate)
        for key, value in resuestDataAsDict.items():
            if key in listToIgnore:
                continue
            setattr(ObjToUpdate, key, value)
        ObjToUpdate.save()
        return (ObjToUpdate.to_dict())

    @classmethod
    def storage_create(cls, listOfReqAttrs, resuestDataAsDict):
        """handles the API post command for all types
        Return Values: dictionary of New Object.
        Exceptions Raised:
        -3: missing Attribute
        -2: invalid Json"""
        if not cls.test_request_data(resuestDataAsDict):
            raise BaseModelInvalidDataDictionary(resuestDataAsDict)
        for attribute in listOfReqAttrs:
            if resuestDataAsDict.get(attribute) is None:
                raise BaseModelMissingAttribute(attribute)
        newObject = cls(**resuestDataAsDict)
        newObject.save()
        return (newObject.to_dict())

    @classmethod
    def test_request_data(cls, requestDataAsDict):
        """used to test if the request data is accurate."""
        if requestDataAsDict is None or type(requestDataAsDict) != dict:
            return (False)
        return (True)

    @staticmethod
    def storage_delete(objectToDelete):
        """handles the API delete command for all types
        return Values: 200: success
        404: invalid object.
        """
        if objectToDelete is None:
            raise BaseModelInvalidObject(objectToDelete)
        objectToDelete.delete()
        models.storage.save()
        return ({})

    @staticmethod
    def storage_get_dict_from_object(ObjToRetrieve):
        """handles the API get command for specific object
        return Values: 200: success
        404: invalid object.
        """
        if ObjToRetrieve is None:
            raise BaseModelInvalidObject(ObjToRetrieve)
        return (ObjToRetrieve.to_dict())

    @staticmethod
    def storage_get_dict_array_from_object_array(arrayOfObjsToRetrieve):
        """handles the API get command for all objects
        return Values: 200: success
        """
        return ([obj.to_dict() for obj in arrayOfObjsToRetrieve])
