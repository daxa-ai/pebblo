from typing import Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class PebbloJsonResponse:
    """
    Response class for custom json response
    """

    @classmethod
    def build(
        cls,
        body: Optional[dict] = None,
        status_code: int = 200,
    ):
        return JSONResponse(status_code=status_code, content=jsonable_encoder(body))
