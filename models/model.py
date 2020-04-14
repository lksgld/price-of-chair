from abc import ABCMeta, abstractmethod
from typing import List, TypeVar, Type, Dict

from common.database import Database

T = TypeVar("T", bound="Model")     # our own type, T must be a Model or one of its subclasses


class Model(metaclass=ABCMeta):     # parent (or super) class
    collection: str       # to get rid off warnings in classmethod
    _id: str

    def __init__(self, *args, **kwargs):    # to get rid off warnings in classmethod
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:     # returns and object of the class, e.g. Item -> Item
        return cls.find_one_by("_id", _id)

    @abstractmethod     # all subclasses have to have this method defined
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: str) -> T:     # Item.find_one_by("url", "https://bla.com")
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: str) -> List[T]:     # Item.find_one_by("url", "https://bla.com")
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
