import logging.config
from importlib import resources
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from pathlib import Path


def setup_logging() -> None:
    path = get_config_path()

    with path.open("rb") as fd:
        config = yaml.safe_load(fd)

    logging.config.dictConfig(config)


def get_config_path() -> Path:
    logging_config = resources.files("server") / "logging.yaml"

    with resources.as_file(logging_config) as path:
        return path
