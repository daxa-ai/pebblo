import logging

from sqlalchemy import JSON, Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

from pebblo.app.config.config import var_server_config_dict
from pebblo.app.enums.common import StorageTypes
from pebblo.app.enums.enums import CacheDir, SQLiteTables
from pebblo.app.utils.utils import get_full_path
from pebblo.log import get_logger

logger = get_logger(__name__)

Base = declarative_base()

config_details = var_server_config_dict.get()


class AiAppTable(Base):
    __tablename__ = SQLiteTables.AI_APP.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDataLoaderTable(Base):
    __tablename__ = SQLiteTables.AI_DATALOADER.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiRetrievalTable(Base):
    __tablename__ = SQLiteTables.AI_RETRIVAL.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDataSourceTable(Base):
    __tablename__ = SQLiteTables.AI_DATASOURCE.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDocumentTable(Base):
    __tablename__ = SQLiteTables.AI_DOCUMENT.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiSnippetsTable(Base):
    __tablename__ = SQLiteTables.AI_SNIPPETS.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiUser(Base):
    __tablename__ = SQLiteTables.AI_USER.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


storage_type = config_details.get("storage", {}).get("type", StorageTypes.FILE.value)

if storage_type == StorageTypes.DATABASE.value:
    # Create an engine that stores data in the local directory's my_database.db file.
    full_path = get_full_path(CacheDir.HOME_DIR.value)
    sqlite_db_path = CacheDir.SQLITE_ENGINE.value.format(full_path)
    if logger.isEnabledFor(logging.DEBUG):
        engine = create_engine(sqlite_db_path, echo=True)
    else:
        engine = create_engine(sqlite_db_path)

    # Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
    Base.metadata.create_all(engine)
