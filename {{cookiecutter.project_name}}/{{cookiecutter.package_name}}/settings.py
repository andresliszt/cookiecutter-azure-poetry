# -*- coding: utf-8 -*-
"""Project settings."""

import logging
from enum import Enum
from enum import IntEnum
from pathlib import Path
from typing import Optional


from dotenv import find_dotenv
from dotenv import load_dotenv
from pydantic import BaseSettings


def init_dotenv():
    """Loc n' load dotenv file.

    Sets the location for a dotenv file containig envvars loads its
    contents.
    Raises:
        FileNotFoundError: When the selected location does not
        correspond to a file.
    Returns:
        Location of the dotenv file.
    """

    candidate = find_dotenv(usecwd=True)

    if not candidate:
        # raise IOError(f"Can't find .env file")
        return

    load_dotenv(candidate)


class LogLevel(IntEnum):
    """Explicitly define allowed logging levels."""

    CRITICAL = logging.CRITICAL
    
    ERROR = logging.ERROR
    
    WARNING = logging.WARNING
    
    INFO = logging.INFO
    
    DEBUG = logging.DEBUG
    
    TRACE = 1 + logging.NOTSET
    
    NOTSET = logging.NOTSET


class LogDest(Enum):
    """Define allowed destinations for logs."""

    CONSOLE = "CONSOLE"
    """Log to console"""
    
    FILE = "FILE"
    """Log to file"""


class LogFormatter(Enum):
    """Define allowed destinations for logs."""

    JSON = "JSON"
    """JSONs, eg for filebeat or similar, for machines."""
    
    COLOR = "COLOR"
    """pprinted, colored, for humans"""


class Settings(BaseSettings):
    """Project settings variables."""

    PACKAGE_PATH = Path(__file__).parent
    """Package path (python files)."""
    
    PROJECT_PATH = PACKAGE_PATH.parent
    """Project path (all files)."""
    
    LOG_PATH: Optional[Path]
    """Path to logfile, only works if ``LOG_DESTINATION=FILE``."""
    
    LOG_FORMAT: LogFormatter = LogFormatter.JSON.value
    """Log style."""
    
    LOG_LEVEL: LogLevel = LogLevel.INFO.value
    """Log level from ``logging`` module."""
    
    LOG_DESTINATION: LogDest = LogDest.CONSOLE.value
    """Destination for logs."""

    class Config:
        """Inner configuration."""

        env_prefix = "{{cookiecutter.package_name}}_".upper()
        use_enum_values = True
