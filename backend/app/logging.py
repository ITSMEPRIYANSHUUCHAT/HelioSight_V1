# app/logging.py
import logging
import sys
import json

def json_formatter(record):
    return json.dumps({
        "time": record.asctime,
        "level": record.levelname,
        "message": record.msg,
        "module": record.module,
        "funcName": record.funcName,
    })

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.getLevelName(settings.LOG_LEVEL))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(json_formatter))
    root.addHandler(handler)