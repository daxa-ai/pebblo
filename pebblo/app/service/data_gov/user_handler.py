import json

from pebblo.app.storage.sqlite_db import SQLiteClient
from pebblo.log import get_logger

logger = get_logger(__name__)


class UserHandler:
    def __init__(self, app_name):
        """
        Constructor for UserHandler class
        :param app_name: App Name
        """
        self.db = SQLiteClient()
        self.app_name = app_name

    def get_user_info(self) -> str:
        """
        This function return user info based on app name
        :return: User Info
        """
        try:
            # create session
            self.db.create_session()
            user_resp = {}
            return json.dumps(user_resp, default=str, indent=4)
        except Exception as ex:
            logger.error(f"Error in getting user info for {self.app_name}. Error: {ex}")
        finally:
            logger.debug(f"Get user info finished for {self.app_name}")
            # Closing session
            self.db.session.close()
