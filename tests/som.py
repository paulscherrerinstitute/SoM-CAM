#!/usr/bin/env python3
""" SoM-CAM comissioning tool

"""
import argparse
import ast
import inspect
import os
import sys

from hw_func import HWFunctions
from utils import *


def main():
    # No traceback
    sys.tracebacklimit=0

    # path to import remote hw_func.py
    

    # logger
    logger = get_logger()
    set_logger_level("DEBUG")

    # parse arguments
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("hostname", help="HW hostname/device", default=os.uname()[1])
    # path_to_functions = '/cfg/hax'
    parser.add_argument('function', help='Name of the function to be executed')
    parser.add_argument('args', nargs='*', help='Arguments for the function.')
    parser.add_argument('--log', '-l', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level.', type=str.upper, default='WARNING')
    parser.add_argument('--doc', '-d', action='store_true')
    # //TODO: update default path to the appropriate folder once in use
    parser.add_argument('--path', '-p', nargs='?', default='/cfg/hax/', help="Folder that contains the hw_func file")
    opt = parser.parse_args()
    # sets debug level
    set_logger_level(opt.log)
    
    logger.info("Starting SoM-CAM comissioning tool...")
    logger.debug(f"Argparse debug: {opt}")
    
    # remote or local
    local_hostname = os.uname()[1]

    # install on remote
    if opt.function.lowercase() == 'install':
        # local
        if opt.hostname == local_hostname:
            try:
                os.system("cd .. && make install")
            except:
                logger.error("Installation failed...")
                raise("Problem during installation")
            quit()
        
        
        


    # try to get the function from the hw_func module
    try:
        func = getattr(HWFunctions, opt.function)
        logger.error(f"Function '{opt.function}' found!")
    except AttributeError:
        logger.error(f"Function '{opt.function}' not found!")
        raise AttributeError(f"The function {opt.function} is not defined.")

    # arguments
    try:
        args = [ast.literal_eval(arg) for arg in opt.args]
    except SyntaxError:
        raise SyntaxError(f"The arguments to {opt.function} "
                          f"were not properly formatted.")

    

    
    if opt.hostname == local_hostname:
        # prints function doc and quits
        if opt.doc:
            logger.debug(f"{opt.hostname} is equal to target. Getting help docstring for {opt.function} locally on {opt.hostname}...")
            logger.debug(f"Docstring request for function: {opt.function}")
            print(inspect.getdoc(func))
            quit()
        logger.debug(f"{opt.hostname} is equal to target. Executing {opt.function} locally on {opt.hostname}...")
        # run the function and pass in the args, print the output to stdout
        func(*args)
    else:
        if opt.doc:
            logger.debug(f"Hostname ({local_hostname}) is not equal to target. Getting help docstring for {opt.function} remotely on {opt.hostname}...")
            logger.debug(f"Docstring request for function: {opt.function}")
            cmd = get_remote_docstring(opt.hostname, opt.path, opt.function)
            logger.debug(f"Command to be executed remotely: {cmd}")
            stdin, stdout, stderr = execute_remote_cmd(
                opt.hostname,
                cmd
            )
        else:
            logger.debug(f"Hostname ({local_hostname}) is not equal to target. Executing {opt.function} remotely on {opt.hostname}...")
            cmd = get_remote_cmd(opt.hostname, opt.path, opt.function, args)
            logger.debug(f"Command to be executed remotely: {cmd}")
            stdin, stdout, stderr = execute_remote_cmd(
                opt.hostname,
                cmd
            )
        # no error
        if len(stderr.read()) == 0:
            print(stdout.read().decode("utf-8"))
            return (True, stdout.read().decode("utf-8"))
        # something went wrong
        print(stdout.read().decode("utf-8"))
        return (False, stdout.read().decode("utf-8"))

if __name__ == "__main__":
    main()
