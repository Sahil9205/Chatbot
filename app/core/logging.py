"""
Centralized Logging Configuration

Every module in the application should obtain its logger
from this module instead of using print().

Example
-------
from app.core.logging import get_logger

logger = get_logger(__name__)

logger.info("Retriever initialized")
"""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:
    """
    Configure the root logger.

    This function should only be called once
    during application startup.
    """

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module.

    Parameters
    ----------
    name : str
        Usually __name__

    Returns
    -------
    logging.Logger
    """

    return logging.getLogger(name)