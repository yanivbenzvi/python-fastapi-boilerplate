import os
import logging

from app.config import settings
from app.utils.log_json_formatter import JsonFormatter


def init_file_handler():
    file_path = os.path.join(settings.log.log_dir, "app.log")
    if not os.path.exists(settings.log.log_dir):
        os.makedirs(settings.log.log_dir)
    file_handler = logging.FileHandler(file_path)
    file_handler.setLevel(logging.DEBUG)

    formatter = JsonFormatter(timestamp=True)
    if settings.log.log_json_format:
        file_handler.setFormatter(formatter)
    else:
        file_handler.setFormatter(logging.Formatter("%(timestamp)s %(message)s"))

    return file_handler


def init_stream_handler():
    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(level=settings.log.log_level)

    formatter = JsonFormatter(timestamp=True)
    if settings.log.log_json_format:
        steam_handler.setFormatter(formatter)
    else:
        steam_handler.setFormatter(logging.Formatter("%(timestamp)s %(message)s"))

    return steam_handler


def init_loggers(app):
    file_handler = init_file_handler()
    stream_handler = init_stream_handler()
    log_level = settings.log.log_level
    app.logger = stream_handler
    # This loop is to set the log level for all loggers and add the handlers
    for v in logging.Logger.manager.loggerDict.values():
        if not isinstance(v, logging.Logger):
            continue

        v.handlers.clear()  # unset all logger handlers
        v.filters.clear()  # unset all logger filters
        v.propagate = True

        if settings.log.only_log_app and not (v.name.startswith("app.") or v.name == "__main__"):
            continue

        v.setLevel(level=log_level)
        v.removeHandler(stream_handler)
        v.addHandler(file_handler)
        v.addHandler(stream_handler)
