__author__ = 'avraham.shukron@gmail.com'

import logging


DEFAULT_STREAM_FORMAT = "%(asctime)s %(name)s %(levelname)s: %(message)s"


__root_logger = logging.getLogger("")


def initialize_root_logger():
    default_stream_handler = logging.StreamHandler()
    default_stream_formatter = logging.Formatter(fmt=DEFAULT_STREAM_FORMAT)
    default_stream_handler.setFormatter(default_stream_formatter)
    __root_logger.addHandler(default_stream_handler)
    __root_logger.setLevel(logging.DEBUG)

initialize_root_logger()


def get_logger(logger_name):
    return logging.getLogger(logger_name)
