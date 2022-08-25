#!/usr/bin/env python3
""" SoM-CAM comissioning tool

"""
import argparse
import inspect
import json
import os
import sys
from cmd.hw_func import HWFunctions
from cmd.som_utils import *
from functools import total_ordering


def main():
    # logger
    logger = get_logger()
    set_logger_level("DEBUG")

    # parse arguments
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("hostname", help="HW hostname/device (local hostname is used by default)", default=os.uname()[1])
    parser.add_argument('function', help='Name of the function to be executed')
    parser.add_argument('args', nargs='*', help='Arguments for the function.')
    parser.add_argument('--log', '-l', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Set the logging level.', type=str.upper, default='WARNING')
    parser.add_argument('--doc', '-d', action='store_true')
    # //TODO: update default path to the appropriate folder once in use
    parser.add_argument('--path', '-p', nargs='?', default='/cfg/hax/', help="Folder that contains the hw_func file.")
    opt = parser.parse_args()
    # sets debug level
    set_logger_level(opt.log)
    
    logger.info("Starting SoM-CAM comissioning tool...")
    logger.debug(f"Argparse debug: {opt}")

    # get_all 
    if opt.function == 'get_all':
        # output file in args
        output_file = opt.args[0]
        if os.path.isfile(output_file):
            logger.info(f"{output_file} exists, it will be overwritten? (Y/N)")
            answer = input()
            if answer not in ['Y', 'y', 'yes', 'YES']:
                error_msg = "Stopping execution..."
                logger.critical(error_msg)
                raise SomCamException(error_msg)
                

        logger.debug("SOM getting all possible functions from HWFunctions()...")
        # locally
        if opt.hostname == os.uname()[1]:
            logger.debug(f"Getting all from local host ({opt.hostname}...")
            
            # get_all_local(HWFunctions)
            get_all_funcs, get_all_args = get_all_local(HWFunctions())
            get_all_dict = {}
            get_all_dict[opt.hostname] = {}
            # iterates over all functions/arguments and
            # creates a dictionary 
            for get_func, get_args in zip(get_all_funcs, get_all_args):
                f = get_function(HWFunctions, get_func)
                args = get_arguments(get_func, getattr(HWFunctions, get_args))
                get_all_dict[opt.hostname][get_func] = f(*args)
            # saves get all in json
            try:
                with open(output_file, "w") as fp:
                    json.dump(get_all_dict,fp, indent=4, sort_keys=True) 
            except IOError:
                error_msg = "Json file couldn't be created."
                logger.critical(error_msg)
                raise SomCamException(error_msg)

        else:
            # remote
            logger.debug(f"Getting all from remote host ({opt.hostname})...")
            list_of_func, list_of_args = get_all_remote(opt.hostname, opt.path)
            remote_dict = {}
            for f, arg in zip(list_of_func, list_of_args):
                cmd = get_remote_cmd(opt.hostname, opt.path, f, "HWFunctions()."+arg)
                logger.debug(f"Command to be executed remotely: {cmd}")
                stdin, stdout, stderr = execute_remote_cmd(
                    opt.hostname,
                    cmd
                )
                results = ast.literal_eval(stdout.read().decode("utf-8").rstrip())
                remote_dict[f] = int(results[0]) if len(results) == 1 else results
            # saves get all in json
            try:
                with open(output_file, "w") as fp:
                    json.dump({opt.hostname: remote_dict}, fp, indent=4, sort_keys=True)
            except IOError:
                error_msg = "Json file couldn't be created."
                logger.critical(error_msg)
                raise SomCamException(error_msg)
    elif opt.function == 'set_all':
        # locally
        if opt.hostname == os.uname()[1]:
            logger.debug(f"Setting all in local host ({opt.hostname}...")
            # loads json file
            input_file_name = opt.args[0]
            if not os.path.isfile(input_file_name):
                error_msg = f"{input_file_name} does not exist, please provide a valid json file."
                logger.critical(error_msg)
                raise SomCamException(error_msg)
            # TODO validates json agains schema 
            # reads json file 
            try:
                logger.info(f"Reading input configuration file {input_file_name}")
                with open(input_file_name, "r") as read_file:
                    configurations = json.load(read_file)
            except IOError:
                error_msg = "Problem loading input configuration file..."
                logger.critical(error_msg)
                raise SomCamException(error_msg)
            problem_flag = []
            for hw, funcs in configurations.items():
                if hw != opt.hostname:
                    error_msg = "Json hostname differs from the hostname. Halting execution..."
                    logger.critical(error_msg)
                    raise SomCamException(error_msg)
                for f in funcs:
                    # default config
                    config_file = [a for a in dir(HWFunctions()) if a.startswith('default_'+f) and not callable(getattr(HWFunctions(), a))][0]
                    # value to be set
                    new_value = configurations[hw][f]
                    # args
                    default_config = [a for a in dir(HWFunctions()) if a.startswith(config_file) and not callable(getattr(HWFunctions(), a))][0]
                    # getting the config file destination
                    default_config_file = get_arguments(f, getattr(HWFunctions, default_config))[0]
                    # set instead of get
                    f = f.replace('get_', 'set_')
                    logger.debug(f"Executing function { f } at hostname { opt.hostname } with the following arguments: { new_value } and default config file {default_config_file}...")
                    # getting the function
                    func = get_function(HWFunctions, f)
                    # executing
                    func(*[new_value, default_config_file])
        else:# remotely
            # loads json file
            input_file_name = opt.args[0]
            # TODO validates json agains schema 
            logger.debug(f"Setting all in remote host {opt.hostname} using { input_file_name }...")
            list_of_func, list_of_args = get_all_remote(opt.hostname, opt.path)
            # reads the remote json
            configurations = {}
            try:
                configurations = json.loads(get_remote_json(opt.hostname, input_file_name))
            except: 
                logger.critical(f"Problem reading remote json file { input_file_name }...")
            # iterate over the functions
            if configurations:
                for hw, funcs in configurations.items():
                    if hw != opt.hostname:
                        error_msg = "Json hostname differs from the hostname. Halting execution..."
                        logger.critical(error_msg)
                        raise SomCamException(error_msg)
                    default_args = get_remote_default_values(opt.hostname, opt.path)
                    for index, f in enumerate(funcs):
                        # get functions and default argument
                        new_value = str(configurations[hw][f])
                        # set instead of get
                        f = f.replace('get_', 'set_')
                        # config file requires double quotes
                        args = [new_value, default_args[index]]
                        logger.debug(f"Executing {f} remotely on {opt.hostname} with arguments: { args }")
                        cmd = get_remote_cmd(opt.hostname, opt.path, f, args)
                        stdin, stdout, stderr = execute_remote_cmd(
                            opt.hostname,
                            cmd
                        )
    else: # individual get/set functions usage
        # desired function to be executed
        func = get_function(HWFunctions, opt.function)
        # arguments for the function
        args = get_arguments(opt.function, opt.args)
        logger.info(f"Executing function {opt.function} with arguments: {args}")
        # local
        if opt.hostname == os.uname()[1]: 
            # prints function doc and quits
            if opt.doc:
                logger.debug(f"{opt.hostname} is equal to target. Getting help docstring for {opt.function} locally on {opt.hostname}...")
                logger.debug(f"Docstring request for function: {opt.function}")
                return (True, inspect.getdoc(func))
            logger.debug(f"{opt.hostname} is equal to target. Executing {opt.function} locally on {opt.hostname}...")
            # run the function and pass in the args, print the output to stdout
            r = func(*args)
            return (True, r)
        else:
            logger.debug(f"Hostname ({os.uname()[1]}) is not equal to target.")
            if opt.doc:
                logger.debug(f"Getting help docstring for {opt.function} remotely on {opt.hostname}...")
                logger.debug(f"Docstring request for function: {opt.function}")
                cmd = get_remote_docstring(opt.hostname, opt.path, opt.function)
            else:
                logger.debug(f"Executing {opt.function} remotely on {opt.hostname}...")
                logger.debug(f"ARGS: { opt.args } ")
                cmd = get_remote_cmd(opt.hostname, opt.path, opt.function, opt.args)
            logger.debug(f"Command to be executed remotely: {cmd}")
            stdin, stdout, stderr = execute_remote_cmd(
                opt.hostname,
                cmd
            )
            r = False
            if len(stderr.read()) == 0:
                # no error
                r = True
            return (r, stdout.read().decode("utf-8"))

if __name__ == "__main__":
    main()
