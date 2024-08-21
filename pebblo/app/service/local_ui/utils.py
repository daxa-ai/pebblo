from pebblo.app.enums.enums import ApplicationTypes
from pebblo.app.models.sqltables import AiAppTable, AiDataLoaderTable


def check_if_loader_app(db, app_name):
    _, ai_loader_app_obj = db.query(
        table_obj=AiDataLoaderTable, filter_query={"name": app_name}
    )
    if ai_loader_app_obj and len(ai_loader_app_obj) > 0:
        return True
    return False


def check_if_retriever_app(db, app_name):
    _, ai_app_obj = db.query(table_obj=AiAppTable, filter_query={"name": app_name})
    if ai_app_obj and len(ai_app_obj) > 0:
        return True
    return False


def get_app_type(db, app_name):
    if check_if_loader_app(db, app_name):
        return ApplicationTypes.LOADER.value
    elif check_if_retriever_app(db, app_name):
        return ApplicationTypes.RETRIEVAL.value
