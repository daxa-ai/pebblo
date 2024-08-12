from sqlalchemy import JSON, Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create an engine that stores data in the local directory's my_database.db file.
engine = create_engine("sqlite:///pebblo.db", echo=True)

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


# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
