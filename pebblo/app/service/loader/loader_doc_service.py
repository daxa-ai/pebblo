from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import LoaderDocResponseModel
from pebblo.app.storage.sqlite_db import SQLiteClient


class AppLoaderDoc:
    def __init__(self):
        self.db = None
        self.data = None
        self.app_name = None

    def process_request(self, data):
        self.db = SQLiteClient()
        self.data = data
        self.app_name = data.get("name")
        message = "Loader Doc API Request processed successfully"

        response = LoaderDocResponseModel(docs=[], message=message)
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=200
        )
