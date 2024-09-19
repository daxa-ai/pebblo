from enum import Enum


class StorageTypes(Enum):
    FILE = "file"
    DATABASE = "db"


class DBStorageTypes(Enum):
    SQLITE = "sqlite"


class ClassificationMode(Enum):
    ALL = "all"
    ENTITY = "entity"
    TOPIC = "topic"
