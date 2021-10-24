# -*- coding: utf-8 -*-
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


class TracebackInfoFilter(logging.Filter):
    """Clear or restore the exception on log records"""

    def __init__(self, name, clear=True):
        super(TracebackInfoFilter, self).__init__(name=name)
        self.clear = clear

    def filter(self, record):
        if self.clear:
            record._exc_info_hidden, record.exc_info = record.exc_info, None
            # clear the exception traceback text cache, if created.
            record.exc_text = None
        elif hasattr(record, "_exc_info_hidden"):
            record.exc_info = record._exc_info_hidden
            del record._exc_info_hidden
        return True


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_file_handler():
    file_handler = RotatingFileHandler(
        "logs/mylog.log", maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    detailed_logger_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(detailed_logger_formatter)
    return file_handler


def get_console_handler():
    console_handler = StreamHandler()
    console_handler.setLevel(logging.INFO)
    concise_logger_formatter = CustomFormatter()
    console_handler.setFormatter(concise_logger_formatter)
    console_handler.addFilter(TracebackInfoFilter("traceback-free"))
    return console_handler


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(get_file_handler())
root_logger.addHandler(get_console_handler())
