import logging
from typing import List, Type

from sqlalchemy import and_, create_engine, func, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm.decl_api import DeclarativeMeta

from pebblo.app.enums.enums import CacheDir
from pebblo.app.storage.database import Database
from pebblo.app.utils.utils import get_full_path, timeit
from pebblo.log import get_logger

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
        if logger.isEnabledFor(logging.DEBUG):
            engine = create_engine(sqlite_db_path, echo=True)
        else:
            engine = create_engine(sqlite_db_path)
        return engine

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close_session(self):
        self.session.close()
        self.session = None

    def delete(self, entry_obj):
        try:
            logger.debug(f"Fetching data for entry {entry_obj}")
            for obj in entry_obj:
                self.session.delete(obj)
                logger.info(f"Entry deleted from {type(obj).__name__} table")
            return True
        except Exception as err:
            logger.error(f"Failed in fetching data, Error: {err}")
            return False

    @timeit
    def insert_data(self, table_obj, data, **kwargs):
        table_name = table_obj.__tablename__
        try:
            logger.debug(f"Insert data into table {table_name}")
            new_record = table_obj(data=data)
            self.session.add(new_record)
            logger.debug("Data inserted into the table.")
            return True, new_record
        except Exception as err:
            logger.error(f"Insert data into table {table_name} failed, Error: {err}")
            return False, err

    @timeit
    def query(self, table_obj, filter_query: dict = {}):
        table_name = table_obj.__tablename__
        try:
            logger.debug(f"Fetching data from table {table_name}")

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

            query = (
                self.session.query(table_obj)
                .filter(and_(*query_conditions))
                .order_by(table_obj.id.desc())
            )
            output = query.all()
            # Return the results
            return True, output

        except Exception as err:
            logger.error(f"Failed in fetching data, Error: {err}")
            return False, err

    @timeit
    def query_by_id(self, table_obj, id):
        # This function is not in use right now, But in the local_ui it will get used.
        table_name = table_obj.__tablename__
        try:
            logger.debug(f"Fetching data from table {table_name}")
            output = self.session.query(table_obj.__class__).filter_by(id=id).first()
            return True, output
        except Exception as err:
            logger.error(
                f"Failed in fetching data from table {table_name}, Error: {err}"
            )
            return False, err

    @timeit
    def query_by_list(
        self,
        table_obj: Type[DeclarativeMeta],
        filter_key: str,
        filter_values: List[str],
    ):
        """
        Pass filter like list. For example get snippets with ids in [<id1>, <id2>]
        :param table_obj: Table object on which query is to be performed
        :param filter_key: Search key
        :param filter_values: List of strings to be added to filter criteria
        """
        table_name = table_obj.__tablename__
        try:
            logger.debug(f"Fetching data from table {table_name}")
            output = (
                self.session.query(table_obj)
                .filter(
                    func.json_extract(table_obj.data, f"$.{filter_key}").in_(
                        filter_values
                    )
                )
                .all()
            )
            return True, output
        except Exception as err:
            logger.error(
                f"Failed in fetching data from table {table_name}, Error: {err}"
            )
            return False, []

    @timeit
    def update_data(self, table_obj, data):
        table_name = table_obj.__tablename__
        try:
            logger.debug(f"Updating Table details, TableName: {table_name}")
            table_obj.data = data
            # Mark the data field as modified, so that it gets updated in the db with commit operation
            flag_modified(table_obj, "data")
            return True, "Data has been updated successfully"
        except Exception as err:
            message = (
                f"Failed in updating app object in table {table_name}, Error: {err}"
            )
            logger.error(message)
            return False, message
