from enum import Enum


class StorageTypes(Enum):
    FILE = "file"
    DATABASE = "db"


class DBStorageTypes(Enum):
    SQLITE = "sqlite"
    MONGODB = "mongodb"
