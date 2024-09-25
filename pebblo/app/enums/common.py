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


class ReportFormat(Enum):
    PDF = "pdf"


class ReportLibraries(Enum):
    XHTML2PDF = "xhtml2pdf"
    WEASYPRINT = "weasyprint"
