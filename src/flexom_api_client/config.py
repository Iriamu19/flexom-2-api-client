import json
import os
from pathlib import Path

from .logger_config import logger


def get_config_vars():
    """Retrieve config from env vars or from JSON config file"""
    config_dict = {"EMAIL": None, "PASSWORD": None}

    config_dict["EMAIL"] = os.getenv("FLEXOM_EMAIL")
    config_dict["PASSWORD"] = os.getenv("FLEXOM_PASSWORD")

    if None not in config_dict.values():
        return config_dict

    config_path = Path.home().joinpath(".config/flexom-api-client/config.json")
    if not config_path.exists():
        logger.error("Config file not found.")
        exit()

    with open(config_path, "r") as file:
        json_config = json.load(file)
    for config_var in config_dict.keys():
        if config_dict[config_var] is None:
            config_dict[config_var] = json_config[config_var]
    return config_dict


config_dict = get_config_vars()
EMAIL = config_dict["EMAIL"]
PASSWORD = config_dict["PASSWORD"]
