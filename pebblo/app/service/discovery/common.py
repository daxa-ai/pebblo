from pebblo.log import get_logger

logger = get_logger(__name__)


def get_or_create_app(db, app_name, load_id, app_class):
    """
    Gets or creates an AiApp.
    """
    logger.info("In Function get_or_create_app")
    exist, ai_app = db.query(app_class, {"name": app_name})
    if exist and ai_app:
        logger.info(f"AiApps: {ai_app}")
        return ai_app

    ai_app = {"name": app_name, "id": load_id}
    response, app_object = db.insert_data(app_class, ai_app)

    if response:
        return app_object
    return False
