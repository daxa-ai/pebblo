# Purpose of this class is, In Future if we want provide option for local hosted database like monogdb, or any other databas
# then in that case, we will need to create a class & implement defined functions without thouching the existing working code.

from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def create_session(self):
        pass

    @abstractmethod
    def close_session(self):
        pass

    @abstractmethod
    def insert_data(self, table_obj, data):
        pass

    @abstractmethod
    def update_data(self, table_obj, data):
        pass

    @abstractmethod
    def delete(self, entry_obj):
        pass

    @abstractmethod
    def query(self, table_obj, condition):
        pass
