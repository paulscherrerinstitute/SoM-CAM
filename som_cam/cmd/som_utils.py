#!/usr/bin/env python3

import ast
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

class SomCamException(Exception):
    pass


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

def get_function(function_class, opt_func):
    # try to get the function from the hw_func module
    try:
        func = getattr(function_class, opt_func)
        logger.debug(f"Function '{opt_func}' found.")
    except AttributeError:
        logger.error(f"Function '{opt_func}' not found.")
        raise AttributeError(f"The function {opt_func} is not defined.")
    return func


def get_arguments(opt_function, opt_args):
    # arguments
    try:
        args = [ast.literal_eval(arg) for arg in opt_args]
    except SyntaxError:
        logger.error(f"The arguments for function '{opt_function}' are not properly formatted.")
        raise SyntaxError(f"The arguments to {opt_function} "
                          f"were not properly formatted.")
    return args


def execute_remote_cmd(hostname, command, username='root', password='root'):
    # ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # connects to remote host
    ssh.connect(hostname, username=username, password=password, timeout=5)
    # executes command
    stdin, stdout, stderr = ssh.exec_command(command, timeout=3, get_pty=True)
    return stdin, stdout, stderr


def get_remote_cmd(hostname: str, path_to_functions: str, function: str, args: list) -> str:
    # creates the cmd str to be executed remotely (cd to path and runs a python cmd)
    return f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'from hw_func import HWFunctions; HWFunctions.{function}(*{args});'"


def get_remote_docstring(hostname: str, path_to_functions: str, function: str) -> str:
    # creates the cmd str to be fetch the docstring for the desired functions
    return f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'from hw_func import HWFunctions; import inspect; print(inspect.getdoc(HWFunctions.{function}));'"

def get_remote_default_values(hostname: str, path_to_functions: str) -> list:
    cmd = f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'import ast; from hw_func import HWFunctions; list_of_args = [getattr(HWFunctions(), a) for a in dir(HWFunctions()) if a.startswith(\"default_\") and not callable(getattr(HWFunctions(), a))]; print(list_of_args);'"
    stdin, stdout, stderr = execute_remote_cmd(hostname, cmd)
    defaults_list = ['\''+value[0]+'\'' for value in ast.literal_eval(stdout.read().decode("utf-8").rstrip())]
    return defaults_list


def get_remote_json(hostname: str, path_json: str) -> str:
    cmd = f"cat { path_json }"
    stdin, stdout, stderr = execute_remote_cmd(hostname, cmd)
    return stdout.read().decode("utf-8").rstrip()


def get_cmd_all_remote(hostname: str, path_to_functions: str):
    # creates the cmd str to fetch all the function and default params from the remote host
    return f"cd /ioc/{hostname}{path_to_functions} && python3 -c 'from hw_func import HWFunctions; list_of_gets = [a for a in dir(HWFunctions()) if a.startswith(\"get_\") and callable(getattr(HWFunctions(), a))]; print(list_of_gets); print(\"&&&\"); list_of_args = [a for a in dir(HWFunctions()) if a.startswith(\"default_\") and not callable(getattr(HWFunctions(), a))]; print(list_of_args);'"


def get_all_local(hw_access_function) -> dict:
    # if filter(lambda a: not a.startswith('__'), dir(obj))
    list_of_gets = [a for a in dir(hw_access_function) if a.startswith('get_') and callable(getattr(hw_access_function, a))]
    list_of_default_args = [a for a in dir(hw_access_function) if a.startswith('default_') and not callable(getattr(hw_access_function, a))]
    return list_of_gets, list_of_default_args


def get_all_remote(hostname: str, path_to_functions: str):
    cmd = get_cmd_all_remote(hostname, path_to_functions)
    stdin, stdout, stderr = execute_remote_cmd(
            hostname,
            cmd)
    list_to_parse = stdout.read().decode("utf-8").split('&&&')
    return ast.literal_eval(list_to_parse[0]), ast.literal_eval(list_to_parse[1]) 


# def set_all_():
#     # TODO
# json is the way to load initially 
