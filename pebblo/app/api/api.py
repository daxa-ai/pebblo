from fastapi import APIRouter, Depends

from pebblo.app.api.req_models import ReqDiscover, ReqLoaderDoc, ReqPrompt, ReqPromptGov
from pebblo.app.config.config import var_server_config_dict
from pebblo.app.service.prompt_gov import PromptGov
from pebblo.app.utils.handler_mapper import get_handler

config_details = var_server_config_dict.get()


class App:
    """
    Controller Class for all the api endpoints for App resource.
    """

    def __init__(self, prefix: str):
        self.router = APIRouter(prefix=prefix)

    @staticmethod
    def discover(
        data: ReqDiscover,
        discover_obj=Depends(lambda: get_handler(handler_name="discover")),
    ):
        # "/app/discover" API entrypoint
        # Execute discover object based on a storage type
        response = discover_obj.process_request(data.model_dump())
        return response

    @staticmethod
    def loader_doc(
        data: ReqLoaderDoc,
        loader_doc_obj=Depends(lambda: get_handler(handler_name="loader")),
    ):
        # "/loader/doc" API entrypoint
        # Execute loader doc object based on a storage type
        response = loader_doc_obj.process_request(data.model_dump())
        return response

    @staticmethod
    def prompt(
        data: ReqPrompt, prompt_obj=Depends(lambda: get_handler(handler_name="prompt"))
    ):
        # "/prompt" API entrypoint
        # Execute a prompt object based on a storage type
        response = prompt_obj.process_request(data.model_dump())
        return response

    @staticmethod
    def promptgov(data: ReqPromptGov):
        # "/prompt/governance" API entrypoint
        prompt_obj = PromptGov(data=data.model_dump())
        response = prompt_obj.process_request()
        return response
