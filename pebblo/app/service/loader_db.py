from pebblo.app.libs.responses import PebbloJsonResponse
from pebblo.app.models.models import LoaderDocResponseModel


class DBLoaderDoc():
    def __init__(self, data):
        self.data = data
        self.app_name = self.data.get("name")

    def process_request(self):
        message = "Loader Doc API Request processed successfully"

        response = LoaderDocResponseModel(docs=[], message=message)
        return PebbloJsonResponse.build(
            body=response.dict(exclude_none=True), status_code=200
        )
    # We can also implement stretegy on loader service, discovery service.