#!/usr/bin/python
# coding=utf-8

# System imports
import sys
from multiprocessing import Process, Pipe
import logging.config

# Libs imports
import numpy as np

# Local imports
from saver import data_saver
from calibration import *


# Define gauss filter values
gauss = np.array([
            0.0447,0.0460,0.0474,0.0488,0.0503,0.0518,0.0533,0.0549,0.0565,
            0.0582,0.0599,0.0616,0.0634,0.0652,0.0670,0.0689,0.0709,0.0728,
            0.0749,0.0770,0.0791,0.0812,0.0835,0.0857,0.0880,0.0904,0.0928,
            0.0953,0.0978,0.1003,0.1030,0.1056,0.1084,0.1111,0.1140,0.1169,
            0.1198,0.1228,0.1259,0.1290,0.1322,0.1354,0.1387,0.1420,0.1454,
            0.1489,0.1524,0.1560,0.1597,0.1634,0.1672,0.1710,0.1749,0.1789,
            0.1829,0.1870,0.1912,0.1954,0.1997,0.2040,0.2084,0.2129,0.2175,
            0.2221,0.2267,0.2315,0.2363,0.2411,0.2461,0.2511,0.2561,0.2613,
            0.2664,0.2717,0.2770,0.2824,0.2878,0.2933,0.2989,0.3045,0.3102,
            0.3160,0.3218,0.3276,0.3336,0.3396,0.3456,0.3517,0.3578,0.3641,
            0.3703,0.3766,0.3830,0.3894,0.3959,0.4024,0.4090,0.4156,0.4222,
            0.4289,0.4357,0.4425,0.4493,0.4562,0.4631,0.4700,0.4770,0.4840,
            0.4910,0.4981,0.5052,0.5123,0.5195,0.5267,0.5338,0.5411,0.5483,
            0.5555,0.5628,0.5701,0.5774,0.5847,0.5920,0.5993,0.6066,0.6139,
            0.6212,0.6285,0.6358,0.6431,0.6503,0.6576,0.6649,0.6721,0.6793,
            0.6865,0.6936,0.7008,0.7079,0.7150,0.7220,0.7290,0.7360,0.7429,
            0.7498,0.7566,0.7634,0.7701,0.7768,0.7834,0.7900,0.7965,0.8029,
            0.8093,0.8156,0.8219,0.8280,0.8341,0.8401,0.8461,0.8519,0.8577,
            0.8634,0.8690,0.8745,0.8799,0.8852,0.8904,0.8955,0.9006,0.9055,
            0.9103,0.9150,0.9196,0.9241,0.9284,0.9327,0.9368,0.9408,0.9447,
            0.9485,0.9522,0.9557,0.9591,0.9624,0.9655,0.9685,0.9714,0.9742,
            0.9768,0.9793,0.9816,0.9839,0.9859,0.9879,0.9897,0.9913,0.9928,
            0.9942,0.9954,0.9965,0.9974,0.9982,0.9989,0.9994,0.9998,1.0000,
            1.0000,1.0000,0.9998,0.9994,0.9989,0.9982,0.9974,0.9965,0.9954,
            0.9942,0.9928,0.9913,0.9897,0.9879,0.9859,0.9839,0.9816,0.9793,
            0.9768,0.9742,0.9714,0.9685,0.9655,0.9624,0.9591,0.9557,0.9522,
            0.9485,0.9447,0.9408,0.9368,0.9327,0.9284,0.9241,0.9196,0.9150,
            0.9103,0.9055,0.9006,0.8955,0.8904,0.8852,0.8799,0.8745,0.8690,
            0.8634,0.8577,0.8519,0.8461,0.8401,0.8341,0.8280,0.8219,0.8156,
            0.8093,0.8029,0.7965,0.7900,0.7834,0.7768,0.7701,0.7634,0.7566,
            0.7498,0.7429,0.7360,0.7290,0.7220,0.7150,0.7079,0.7008,0.6936,
            0.6865,0.6793,0.6721,0.6649,0.6576,0.6503,0.6431,0.6358,0.6285,
            0.6212,0.6139,0.6066,0.5993,0.5920,0.5847,0.5774,0.5701,0.5628,
            0.5555,0.5483,0.5411,0.5338,0.5267,0.5195,0.5123,0.5052,0.4981,
            0.4910,0.4840,0.4770,0.4700,0.4631,0.4562,0.4493,0.4425,0.4357,
            0.4289,0.4222,0.4156,0.4090,0.4024,0.3959,0.3894,0.3830,0.3766,
            0.3703,0.3641,0.3578,0.3517,0.3456,0.3396,0.3336,0.3276,0.3218,
            0.3160,0.3102,0.3045,0.2989,0.2933,0.2878,0.2824,0.2770,0.2717,
            0.2664,0.2613,0.2561,0.2511,0.2461,0.2411,0.2363,0.2315,0.2267,
            0.2221,0.2175,0.2129,0.2084,0.2040,0.1997,0.1954,0.1912,0.1870,
            0.1829,0.1789,0.1749,0.1710,0.1672,0.1634,0.1597,0.1560,0.1524,
            0.1489,0.1454,0.1420,0.1387,0.1354,0.1322,0.1290,0.1259,0.1228,
            0.1198,0.1169,0.1140,0.1111,0.1084,0.1056,0.1030,0.1003,0.0978,
            0.0953,0.0928,0.0904,0.0880,0.0857,0.0835,0.0812,0.0791,0.0770,
            0.0749,0.0728,0.0709,0.0689,0.0670,0.0652,0.0634,0.0616,0.0599,
            0.0582,0.0565,0.0549,0.0533,0.0518,0.0503,0.0488,0.0474,0.0460,
            0.0447
    ])

def process_data(pipeline, samples, path='./'):
    '''
    Process data from sensor. Accordingly get n samples and calculate average
    value from this samples. Then use Gauss filter and finally make 
    calibration.

    Args:
        pipeline: pipeline where from this function will receive samples
        samples: number of samples per second
        path: path where we will save our files
    '''
    logger = logging.getLogger(__name__)

    # Data set [[H], [Z], [E], [T]]
    buffersize = 2*samples + 1
    data_set = np.zeros((buffersize, 4))
    # Number of samples
    number_of_samples = 0
    # Get time for every second saving
    firsttime = datetime.datetime.now()

    # Create pipeline for communication with 'saver'
    parent_conn, child_conn = Pipe(True)
    # Create new process for data saver.
    data_saver_proc = Process(target=data_saver, 
            args=(child_conn, path))
    data_saver_proc.start()

    # Start main cycle
    try:
        while True:
            # Get data from pipeline
            data = pipeline.recv()    

            # Get current time 
            currtime = datetime.datetime.now()

            if data:
                # If needed to save non calibrated data
                # try:
                    # save_data(result, path=path, suffix='')
                # except:
                    # logger.error('Error occured while saving original data.')


                # If array isn't full add new line
                if number_of_samples < buffersize:
                    data_set[number_of_samples] = data
                    number_of_samples += 1
                else:
                    # Otherwise make roll and calculate calibrated values
                    np.roll(data_set, 1)
                    data_set[0] = data

                    # Calculate mean value and make calibration
                    mean_value = find_mean(data_set, gauss)
                    result = calibrate(mean_value)

                    # Send calibrated data to 'saver' process.
                    if currtime.microsecond < firsttime.microsecond:
                        parent_conn.send(result) 

                    firsttime = currtime
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt in process \'processor\'.')
        sys.exit(0)
