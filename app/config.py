import logging
import os
from os.path import exists
from omegaconf import OmegaConf

logger = logging.getLogger(__name__)


def __load_if_exists(path: str):
    if exists(path):
        logger.debug("Loading configuration", extra={"file": path})
        return OmegaConf.load(path)
    else:
        logger.debug("Configuration file does not exists", extra={"file": path})
        return OmegaConf.create()


def __init_settings():
    conf = OmegaConf.merge(
        __load_if_exists("app/resources/settings.conf.yaml"),
    )
    OmegaConf.set_readonly(conf, True)
    logger.debug("Loaded all configuration settings")
    return conf


settings = __init_settings()
