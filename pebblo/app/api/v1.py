from fastapi import APIRouter

from pebblo.app.api.req_models import ReqClassifier
from pebblo.app.config.config import var_server_config_dict
from pebblo.app.service.classification import Classification

config_details = var_server_config_dict.get()


class APIv1:
    """
    Controller Class for all the api endpoints for App resource.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def classify_data(data: ReqClassifier):
        # "/classify" API entrypoint
        # Execute entity/topic classification
        cls_obj = Classification(data.model_dump())
        response = cls_obj.process_request()
        return response
