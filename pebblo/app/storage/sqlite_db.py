from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from pebblo.app.enums.enums import CacheDir
from pebblo.app.storage.database import Database
from pebblo.app.utils.utils import get_full_path
from pebblo.log import get_logger

from ..enums.enums import CacheDir
from ..utils.utils import get_full_path
from .database import Database

logger = get_logger(__name__)


class SQLiteClient(Database):
    def __init__(self):
        engine = self._create_engine()
        super().__init__(engine=engine)
        self.session = None

    @staticmethod
    def _create_engine():
        # Create an engine that stores data in the local directory's db file.
        full_path = get_full_path(CacheDir.HOME_DIR.value)
        sqlite_db_path = CacheDir.SQLITE_ENGINE.value.format(full_path)
        engine = create_engine(sqlite_db_path, echo=True)
        return engine

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
