from enum import Enum


class StorageTypes(Enum):
    FILE = "file"
    DATABASE = "db"


class DBStorageTypes(Enum):
    SQLITE = "sqlite"
    MONGODB = "mongodb"


class ClassificationMode(Enum):
    ALL = "all"
    ENTITY = "entity"
    TOPIC = "topic"
