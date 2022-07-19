#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)
# create console handler and set level to debug
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


def get_logger():
    """Get the logger instance of the current som_cam execution."""
    return logger


def set_logger_level(level_str):
    """Sets the logger instance of SoM-CAM
    
    Args:
        level_str (str): The new verbose level of the logger 
            Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL 
    """
    logger = get_logger()
    new_logger_level = getattr(logging, level_str)
    logger.setLevel(new_logger_level)


def update_logger(verbose):
    """Updates the logger instance of SoM-CAM level
    
    Args:
        verbose (str): The new verbose level of the logger 
            Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL 
    """
    if verbose is not None:
        verbose = verbose.upper()
        set_logger_level(verbose)
