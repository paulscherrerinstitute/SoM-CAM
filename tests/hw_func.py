#!/usr/bin/env python3
# coding: utf-8
import getpass
import logging


class HWFunctions:

    @staticmethod
    def set_voltage(value: int, config_file: str) -> bool:
        '''
        \n Function set_voltage helper:

        Usage: ./som.py set_voltage value config_file

        Args:
            - value (int): value for the voltage
            - config_file (str): path to the file that contains the value for the voltage

        Returns:
            True if successful or False if not successful


        Description:
            This function does sets the defined voltage to the config file in the hw.
        \n
        '''

        # Add configuration code here
        with open(config_file, 'w') as f:
            f.write(str(value))
        return True
    
    @staticmethod
    def get_voltage(config_file: str) -> list:
        '''
        \n Function get_voltage helper:

        Usage: ./som.py get_voltage config_file

        Args:
            - config_file (str): path to the file that contains the value for the voltage

        Returns:
            Content of the config_file with the defined voltage 


        Description:
            This function gets the defined voltage from the config file in the hw.
        \n
        '''
        with open(config_file) as f:
            contents = f.readlines()
        return contents

    @staticmethod
    def get_this():
        return 0

    @staticmethod
    def get_that():
        return 0

