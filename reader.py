#!/usr/bin/python
# coding=utf-8

# System imports
import time
import sys
import logging.config

# Libs imports
import serial
from serial import SerialException
from settings import config

logger = logging.getLogger(__name__)

def init_communication(port='/dev/ttyAMA0', baudrate=115200, timeout=None):
    '''
    This function create Serail communication object with default parameters:

    Args:
        port: serial port. By default '/dev/ttyAMA0'
        baudrate: By default 115200
        timeout: By default 'None'
    Returns:
        pyserial object to communicate with device
    '''

    try:
        inpoint = serial.Serial(port, baudrate=baudrate, timeout=timeout)

        return inpoint
    except SerialException:
        logger.error('Fail to open the port. Exiting.')
        sys.exit(1)

def start_sensor(inpoint):
    '''
    This function send start command to sensor ('CN').

    Args:
        inpoint: pyserial object
    Returns:
        True if start is successful otherwise False.
    '''
    try:
        inpoint.write(config['start_cmd'])
        time.sleep(1)
        return True
    except SerialException:
        logger.error('Fail to start the sensor.')
        return False

def stop_sensor(inpoint):
    '''
    Send stop command to sensor ('CS'). And return true if writing 
    is successful.

    Args:
        inpoint: pyserial object
    Returns:
        True if stop is successful otherwise False.
    '''

    try:
        inpoint.write(config['stop_cmd'])
        time.sleep(1)
        return True
    except SerialExcetption:
        logger.error('Fail to stop the sensor.')
        return False

def readline(inpoint):
    '''
    Read one line from sensor.

    Args:
        inpoint: pyserial object
    Returns:
        line or False
    '''
    try:
        return inpoint.readline()
    except SerialException:
        logger.error('Fail to read from the sensor.')
        return False

