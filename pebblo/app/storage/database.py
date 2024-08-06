# Purpose of this class is, In Future if we want provide option for local hosted database like monogdb, or any other databas
# then in that case, we will need to create a class & implement defined functions without thouching the existing working code.

from abc import ABC, abstractmethod


class Database(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def insert(self, query):
        pass

    @abstractmethod
    def update(self, query):
        pass

    @abstractmethod
    def upsert(self, query):
        pass

    @abstractmethod
    def delete(self, query):
        pass

    @abstractmethod
    def create(self, query):
        pass
