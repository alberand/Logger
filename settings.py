#!/usr/bin/python
# coding=utf-8

#
# ./settings.py
#

# This file contains configurations

# Basic program configurations
config = {
    # Number of samples per second
    'samples': 207,

    # Turn on debug mode. In this mode program will send some debug information
    # to its stdout and use GPIO output to mark reading cycle.
    'debug': False,

    # GPIO pin used in 'debug' mode.
    'debug_pin': 4,

    # Path where should be stored all received and calculated data
    'path': './data/',

    # Default configuration for serial port
    'port': '/dev/ttyAMA0',
    'baudrate': 115200,
    'timeout': 3,

    # Communication with device
    'start_cmd': b'CN',
    'stop_cmd': b'CS',

    # Files' names format
    'file_name_format': '%Y-%m-%d'
}

# Calibration data
cal_config = {
    # The compensation field
    'comp': [2.6580E-5,  3.7380E-5,  0],

    # Offsets
    'ofs': [-2338, -632, -1823],

    # Sensivity
    'sen': [1.8802E+12, 1.8714E+12, 1.8583E+12],

    # The orthogonalization matrix
    'ort_mat': [
        [1,             0,              0           ],
        [0.003272853,   1.000005356,    0           ],
        [-0.008173561,  -0.023780785,   1.000315443 ]
    ]

}
