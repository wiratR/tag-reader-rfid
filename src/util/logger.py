# setup_logger.py
from dotenv import load_dotenv
import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

FORMATTER = logging.Formatter(
    "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s")


app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
config_path = os.path.join(app_path, "config")
log_path = os.path.join(app_path, "log")
LOG_FILE = os.path.join(log_path, "app.log")
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)
open(LOG_FILE, "w")

dotenv_path = os.path.join(config_path, ".env")
load_dotenv(dotenv_path)
LOG_LEVEL_DEBUG = (os.getenv("LOG_LEVEL_DEBUG") == 'true')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_rotating_file_handler():
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=2000000, backupCount=10)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    # better to have too much log than not enough
    if LOG_LEVEL_DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_rotating_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger