from pebblo.app.enums.enums import ApplicationTypes
from pebblo.app.utils.utils import timeit
from pebblo.log import get_logger

logger = get_logger(__name__)


@timeit
def get_or_create_app(db, app_name, app_class, data, app_type):
    """
    Gets or creates an AiApp
    """
    try:
        logger.debug(f"Fetching or creating {app_class.__tablename__} details")

        ai_app = {"name": app_name}

        if app_type == ApplicationTypes.LOADER.value:
            ai_app["id"] = data["load_id"]
        elif app_type == ApplicationTypes.RETRIEVAL.value:
            pass

        exist, existing_ai_app = db.query(app_class, ai_app)
        if exist and existing_ai_app:
            logger.debug(f"Application details exists in {app_class.__tablename__}")
            return existing_ai_app[0]

        logger.debug(
            f"Application details does not exists in {app_class.__tablename__}"
        )

        # Inserting app details
        response, app_object = db.insert_data(app_class, ai_app)

        if response:
            logger.debug(
                f"Fetching or creating {app_class.__tablename__} details finished."
            )
            return app_object
    except Exception as err:
        logger.error(
            f"Failed in fetching and creating app in {app_class.__tablename__} object. Error: {err}"
        )
        raise Exception(err)
