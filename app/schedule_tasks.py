import logging
import traceback

from fastapi_utils.tasks import repeat_every

logger = logging.getLogger(__name__)


def check_if_all_tasks_finished():
    """
    Check if all tasks are finished.
    """
    logger.info("Finished checking if all tasks are finished")


def send_batched_logs_to_db():
    """
    Send batched logs to db.
    not implemented yet
    """
    logger.info("Finished sending logs to db", extra={"batch_size": 0})


def init_schedule_tasks(app):
    """
    Initialize schedule tasks, which are run periodically.
    :param app:
    """

    @app.on_event("startup")
    @repeat_every(seconds=60 * 60)
    def send_logs_to_db():
        try:
            send_batched_logs_to_db()
        except Exception as e:
            logger.critical("Error sending logs to db", extra={
                "error": str(e),
                "traceback": traceback.format_exc()
            })

    # graceful shutdown
    @app.on_event("shutdown")
    def shutdown():
        try:
            check_if_all_tasks_finished()
        except Exception as e:
            logger.critical("Error shutting down", extra={
                "error": str(e),
                "traceback": traceback.format_exc()
            })
