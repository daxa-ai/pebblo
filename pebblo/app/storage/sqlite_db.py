from sqlalchemy import and_, create_engine, text
from sqlalchemy.orm import sessionmaker

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
        table_name = table_obj.__tablename__
        try:
            logger.info(f"Insert data into table {table_name}, Data: {data}")
            new_record = table_obj(data=data)
            self.session.add(new_record)
            logger.info("Data inserted into the table.")
            return True, new_record
        except Exception as err:
            logger.info(f"insert data into table {table_name} failed, Error: {err}")
            return False, err

    def query(self, table_obj, filter_query: dict):
        table_name = table_obj.__tablename__
        try:
            logger.info(f"Fetching data from table {table_name}")
            logger.debug(f"Filter Condition: {filter_query}")

            json_column = "data"

            # Dynamically build the filter conditions and parameters
            query_conditions = []
            for key, value in filter_query.items():
                # Format the JSON path for SQLite
                json_path = f"$.{key}"
                json_value = f"{value}"

                # Construct condition string
                condition_str = (
                    f"json_extract({json_column}, '{json_path}') = '{json_value}'"
                )
                query_conditions.append(text(condition_str))

            query = self.session.query(table_obj).filter(and_(*query_conditions))
            output = query.first()
            # Return the results
            return True, output

        except Exception as err:
            logger.error(f"Failed in fetching data, Error: {err}")
            return False, err

    def query_by_id(self, table_obj, id):
        # This function is not in use right now, But in local ui it will get used.
        table_name = table_obj.__tablename__
        try:
            logger.info(f"Fetching data from table {table_name}")
            output = self.session.query(table_obj.__class__).filter_by(id=id).first()
            return True, output
        except Exception as err:
            logger.error(
                f"Failed in fetching data from table {table_name}, Error: {err}"
            )
            return False, err

    def update_data(self, table_obj, data):
        table_name = table_obj.__tablename__
        try:
            logger.info(f"Updating Table details, TableName: {table_name}")
            logger.debug(f"New Updated data: {data}")
            table_obj.data = data
            self.session.add(table_obj)
            return True, "Data has been updated successfully"
        except Exception as err:
            message = (
                f"Failed in updating app object in table {table_name}, Error: {err}"
            )
            logger.error(message)
            return False, message
