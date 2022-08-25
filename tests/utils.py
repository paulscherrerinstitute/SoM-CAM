#!/usr/bin/env python3

import getpass
import logging

import paramiko

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

def execute_remote_cmd(hostname, command):
    # ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # result = ssh.connect(hostname, 22, username=username, password=GetCreds(username), auth_timeout=30, look_for_keys=True)
    ssh.connect(hostname, username='root', password='root', timeout=5)
    stdin, stdout, stderr = ssh.exec_command(command, timeout=3, get_pty=True)

    # stdin, stdout, stderr = ssh.exec_command('/sbin/ifconfig') -> simple exec ex.
    return stdin, stdout, stderr
    # return stdout.read().decode("utf-8")


def get_remote_cmd(hostname: str, path_to_functions: str, function: str, args: list) -> str:
    return f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'from hw_func import HWFunctions; HWFunctions.{function}(\"{args[0]}\");'"


def get_remote_docstring(hostname: str, path_to_functions: str, function: str) -> str:
    return f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'from hw_func import HWFunctions; import inspect; print(inspect.getdoc(HWFunctions.{function}));'"

