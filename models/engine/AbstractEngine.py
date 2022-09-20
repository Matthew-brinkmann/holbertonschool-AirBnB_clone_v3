from abc import ABC, abstractmethod


class AbstractEngine(ABC):
    @abstractmethod
    def all(self, cls=None):
        pass

    @abstractmethod
    def new(self, obj):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self, obj=None):
        pass

    @abstractmethod
    def reload(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get(self, cls, id):
        pass

    @abstractmethod
    def count(self, cls=None):
        pass