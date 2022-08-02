#!/usr/bin/env python3
# coding: utf-8

from .utils import get_logger, remote_cmd

log = get_logger()


def set_current_bias(value, channel):
    # print("Setting current bias to " + str(value))
    # Add configuration code here
    return False


def set_voltage_bias(value, channel):

    return True


def set_bandwidth(value, channel):
    # print("Setting bandwidth to " + str(value))
    # Add configuration code here
    return True


def set_matrix_level0(value, channel):
    for index in value:
        log.debug("Enabling matrix input " + str(index))
        # Add configuration code here
    return True


def set_matrix_level1(value, channel):
    for index in value:
        log.debug("Enabling matrix input " + str(index))
        # Add configuration code here
    return True


def set_hv_out(value, channel):
    # print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True


def set_hv_alarm_current(value, channel):
    # print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True


def set_hv_alarm_volt_min(value, channel):
    # print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True


def set_hv_alarm_volt_max(value, channel):
    # print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True


def set_example_voltage(cmd, username, password, hostname):

    stdin, stdout, stderr = remote_cmd(
        # "129.129.130.168", "cd /ioc/XCZU6EG-AD82 && ls -l"
        # "129.129.130.168",
        username,
        password,
        hostname,
        cmd,
    )
    print()
    # no error
    if len(stderr.read()) == 0:
        return (True, stdout.read().decode("utf-8"))
    # something went wrong
    return (False, stdout.read().decode("utf-8"))
