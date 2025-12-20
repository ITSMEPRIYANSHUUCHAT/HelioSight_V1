# app/logging.py

import logging
import sys
from app.config import settings


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging():
    root = logging.getLogger()
    root.setLevel(settings.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root.handlers.clear()
    root.addHandler(handler)
