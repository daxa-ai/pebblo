from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

# Create an engine that stores data in the local directory's my_database.db file.
engine = create_engine('sqlite:///pebblo.db', echo=True)


Base = declarative_base()


class AiAppsTable(Base):
    __tablename__ = 'aiapps'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)


# Create all tables in the engine. This is equivalent to "Create Table" statements in raw SQL.
Base.metadata.create_all(engine)
