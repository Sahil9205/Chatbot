"""
Centralized Logging Configuration
=================================

This module provides a centralized logging configuration for the
entire application.

Why?
----
Instead of using print() statements throughout the project, every
module should obtain a logger from this file.

Benefits
--------
- Consistent logging format
- Logs displayed in the terminal
- Logs stored in a file
- Easier debugging
- Single place to manage logging configuration

Example
-------
from app.core.logging import configure_logging, get_logger

configure_logging()

logger = get_logger(__name__)

logger.info("Retriever initialized")
logger.warning("Embedding model not found.")
logger.error("Database connection failed.")
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure the application's logging system.

    This function should be called only once during
    application startup (main.py).

    Parameters
    ----------
    level : int
        Logging level (default: logging.INFO)
    """

    # ------------------------------------------------------------------
    # Create the logs directory
    # ------------------------------------------------------------------

    project_root = Path(__file__).resolve().parents[2]
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # Create a unique log file for every application run
    # ------------------------------------------------------------------

    log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_file_path = logs_dir / log_file_name

    # ------------------------------------------------------------------
    # Configure logging
    # ------------------------------------------------------------------

    logging.basicConfig(
        level=level,

        format=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "Line:%(lineno)d | "
            "%(message)s"
        ),

        datefmt="%Y-%m-%d %H:%M:%S",

        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                filename=log_file_path,
                encoding="utf-8"
            ),
        ],

        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module.

    Parameters
    ----------
    name : str
        Usually __name__.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """

    return logging.getLogger(name)