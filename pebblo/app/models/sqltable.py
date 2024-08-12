from sqlalchemy import JSON, Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

from pebblo.app.enums.enums import CacheDir
from pebblo.app.utils.utils import get_full_path

# Create an engine that stores data in the local directory's my_database.db file.

full_path = get_full_path(CacheDir.HOME_DIR.value)
sqlite_db_path = CacheDir.SQLITE_ENGINE.value.format(full_path)
engine = create_engine(sqlite_db_path, echo=True)

Base = declarative_base()


class AiAppTable(Base):
    __tablename__ = "aiapp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDataLoaderTable(Base):
    __tablename__ = "aidataloader"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiRetrievalTable(Base):
    __tablename__ = "airetrieval"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDataSourceTable(Base):
    __tablename__ = "aidatasource"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiDocumentTable(Base):
    __tablename__ = "aidocument"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


class AiSnippetsTable(Base):
    __tablename__ = "aisnippets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
