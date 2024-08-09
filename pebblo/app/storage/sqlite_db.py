from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from pebblo.log import get_logger

from .database import Database

logger = get_logger(__name__)


class SQLiteClient(Database):
    def __init__(self):
        super().__init__()
        # Create an engine that stores data in the local directory's my_database.db file.
        self.engine = create_engine("sqlite:///pebblo.db", echo=True)
        self.session = None

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_session(self):
        self.session.close()
        self.session = None

    def delete(self, query):
        pass

    def insert_data(self, table_obj, data, **kwargs):
        try:
            logger.info(f"Insert data into table {table_obj}, Data: {data}")
            if table_obj.__name__ == "AiRetrievalTable":
                new_record = table_obj(data=data, app_id=kwargs.get("app_id"))
            else:
                new_record = table_obj(data=data)
            self.session.add(new_record)
            logger.info("Data inserted into the table.")
            return True, new_record
        except Exception as err:
            logger.info(f"insert data into table {table_obj} failed, Error: {err}")
            return False, err

    def query(self, table_obj, condition: dict = None):
        try:
            logger.info(f"Fetching data from table {table_obj}")
            # Initialize base query

            if condition:
                query = self.session.query(table_obj)
                for key, value in condition.items():
                    # Build the filter condition dynamically using JSON path
                    query = query.filter(
                        func.json_extract(table_obj.data, f"$.{key}") == value
                    )
                # Execute the query and fetch results
                output = query.first()
            # if condition:
            #     output = self.session.query(table_obj).filter_by(**condition).first()
            else:
                # Query the table
                output = self.session.query(table_obj).first()
            return True, output
        except Exception as err:
            logger.error(f"Failed in fetching data from table, Error: {err}")
            return False, err

    def update_data(self, table_obj, data):
        try:
            logger.info("Updating aiapp details")
            logger.debug(f"New Updated data: {data}")
            table_obj.data = data
            return True, "Data has been updated successfully"
        except Exception as err:
            message = f"Failed in updating app object in table, Error: {err}"
            logger.error(message)
            return False, message
