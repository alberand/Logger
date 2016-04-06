#!/usr/bin/python
# coding=utf-8

# System imports
import sys
import time
import datetime
import logging.config

# Installed libs
import numpy as np
from settings import config
from settings import cal_config
 
logger = logging.getLogger(__name__)
# logger = []

def save_data(data, path, suffix=''):
    '''
    Save data to path/%Y-%m-%d_suffix.txt

    Args:
        data: some data (For example: 123 123 123)
        path: path where to save file (For example: ./data/)
        suffix: suffix for filename (For example for suffix 'original' filename
            will be 2015-12-24_original.txt)

    '''
    currtime = datetime.datetime.now()
    filename = path + currtime.strftime(config['file_name_format']) \
            + '_' + str(suffix) + '.txt'
    logger.info('Filename: ' + str(filename))
    # a - open for writing, appending to the end of the file if it exists
    # 1 - line buffering
    with open(filename, 'a', 1) as f:
        f.write(str(data) + '\n')

def parse_data_string(string):
    '''
    Cut string from sensors to separate values.

    Args:
        string: string in format like this '1234567123456712345671234567'
    Returns:
        [1234567, 1234567, 1234567, 1234567]
    '''
    return [string[0:7], string[9:17], string[18:26], string[27:35]]

def calibrate(data):
    '''
    This function calibrate data and return numpy array. (np is numpy)

    Args:
        data: is list with 3 items. For example: np.array([123, 456, 789])
    Returns:
        np.array([111, 444, 777]) array with calibrated data
    '''
    raw = data[0:3]

    # The compensation field
    comp = np.array(cal_config['comp'])
    # Offsets
    ofs  = np.array(cal_config['ofs'])
    # Sensivity
    sen  = np.array(cal_config['sen'])
    # The orthogonalization matrix
    P = np.array(cal_config['ort_mat'])

    # Just calculate value in engineering units
    eu = raw - ofs
    B = np.array(1/sen*eu)
    # Value in nT
    M = np.dot(P, B)
    # Add compensation
    M = M + comp
    M = list(M)
    M.append(data[3])

    return M

def find_mean(data, gauss):
    '''
    This function apply gauss filter to data and then calculate mean value. And
    multiply it by 2.

    Args:
        data: np.array([[H], [Z], [E], [T]]). H, Z, E and T are arrays
    Returns:
        np.array([[H], [Z], [E], [T]])
    '''
    return np.mean(gauss[np.newaxis, :].T*data, axis=0)*2

