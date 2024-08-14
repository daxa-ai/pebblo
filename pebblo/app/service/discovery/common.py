from pebblo.app.enums.enums import ApplicationTypes
from pebblo.log import get_logger

logger = get_logger(__name__)


def get_or_create_app(db, app_name, app_class, data, app_type):
    """
    Gets or creates an AiApp.
    """
    try:
        logger.info(f"Fetching or creating {app_class} details")
        exist, ai_app = db.query(app_class, {"name": app_name})
        if exist and ai_app:
            logger.info(f"AiApps: {ai_app}")
            return ai_app

        ai_app = {"name": app_name}
        if app_type == ApplicationTypes.LOADER.value:
            ai_app["id"] = data["load_id"]
        elif app_type == ApplicationTypes.RETRIEVAL.value:
            pass

        response, app_object = db.insert_data(app_class, ai_app)

        if response:
            logger.info(f"Fetching or creating {app_class} details finished.")
            return app_object
    except Exception as err:
        logger.error(
            f"Failed in fetching and creating {app_class} object. Error: {err}"
        )
        return False
