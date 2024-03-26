import json
from typing import Optional

from pebblo.app.libs.logger import logger


class PebbloJsonResponse:
    """
    Response class for custom json response
    """
    media_type = "application/json"

    def __init__(
            self,
            body: Optional[dict] = None,
            status_code: int = 200,
            headers: Optional[dict] = None
    ):
        if body is None:
            body = {}
        if not headers:
            headers = {'Content-Type': 'application/json'}
        else:
            headers.update({'Content-Type': 'application/json'})

        self.response = {
            "statusCode": status_code,
            "headers": headers,
            # "body": json.dumps(body, default=str)
            "body": body
        }
        logger.debug(f"Sending Response : {self.response}")

    @classmethod
    def build(cls, body: Optional[dict] = None, status_code: int = 200, headers: Optional[dict] = None):
        response = cls(body, status_code, headers)
        return response.response
