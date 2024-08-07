from .database import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pebblo.log import get_logger
logger = get_logger(__name__)


class SQLiteClient(Database):

    def __init__(self):
        super().__init__()
        # Create an engine that stores data in the local directory's my_database.db file.
        self.engine = create_engine('sqlite:///pebblo.db', echo=True)
        self.session = None

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_session(self):
        self.session.close()
        self.session=None

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

    def insert_data(self, table_obj, data):
        try:
            logger.info(f"Insert data into table {table_obj}, Data: {data}")
            new_record = table_obj(data=data)
            self.session.add(new_record)
            logger.info("Data inserted into the table.")
            return True, "Data inserted into the table"
        except Exception as err:
            logger.info(f"insert data into table {table_obj} failed, Error: {err}")
            return False, err

    def get_objects(self, table_obj):
        try:
            logger.info(f"Fetching data from table {table_obj}")
            # Query the table
            output = self.session.query(table_obj).all()
            return True, output
        except Exception as err:
            logger.error(f"Failed in fetching data from table, Error: {err}")
            return False, err
