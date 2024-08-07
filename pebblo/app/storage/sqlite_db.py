from .database import Database
from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.orm import sessionmaker

from ..models.sqltable import AiAppsTable


class SQLiteClient(Database):

    def __init__(self):
        super().__init__()
        # Create an engine that stores data in the local directory's my_database.db file.
        engine = create_engine('sqlite:///my_database.db', echo=True)

        # Create a new session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert(self, query):
        pass

    def update(self, query):
        pass

    def upsert(self, query):
        pass

    def delete(self, query):
        pass

    def create(self, query):
        pass

    def insert_ai_app(self, ai_apps):
        print("Insert Into AiAPps")
        new_record = AiAppsTable(data=ai_apps)
        self.session.add(new_record)
        self.session.commit()

        # Close the session
        self.session.close()

    def get_ai_apps(self, table_name):

        # Query the table
        output = self.session.query(table_name).all()
        return output
