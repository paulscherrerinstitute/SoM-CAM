#!/usr/bin/env python3
# coding: utf-8


def set_current_bias(value, channel):
    print("Setting current bias to " + str(value))
    # Add configuration code here
    return True

def set_voltage_bias(value, channel):
    print("Setting voltage bias to " + str(value))
    # Add configuration code here
    return True

def set_bandwidth(value, channel):
    print("Setting bandwidth to " + str(value))
    # Add configuration code here
    return True

def set_matrix_level0(value, channel):
    for index in value:
        print("Enabling matrix input " + str(index))
        # Add configuration code here
    return True

def set_matrix_level1(value, channel):
    for index in value:
        print("Enabling matrix input " + str(index))
        # Add configuration code here
    return True

def set_hv_out(value, channel):
    print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True

def set_hv_alarm_current(value, channel):
    print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True

def set_hv_alarm_volt_min(value, channel):
    print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True

def set_hv_alarm_volt_max(value, channel):
    print("Setting high-voltage output to " + str(value))
    # Add configuration code here
    return True
