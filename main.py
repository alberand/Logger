#!/usr/bin/python
# coding=utf-8

# System imports
import sys
import time
import logging.config
from multiprocessing import Process, Pipe


# Local imports
from reader import *
from processor import process_data
from calibration import parse_data_string
from generator import Generator
from settings import config

if __name__ == '__main__':
    # Load the logging configuration
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger(__name__)

    # Path where should be stored all received and calculated data
    path = config['path']
    # Number of samples per second
    samples = config['samples']

    # Initialize port communication with sensor
    # Virtual mode mean that we don't have a real sensor and we will just
    # generate random numbers. Its mode used for testing.
    virtual = False
    if 'virtual' in sys.argv:
        logger.info('Run in virtual mode.')
        virtual = True
        inpoint = Generator()
    else:
        logger.info('Run in normal mode.')
        inpoint = init_communication()
        if not start_sensor(inpoint):
            sys.exit(0)
        # A few reading
        readline(inpoint)
        readline(inpoint)

    # GPIO setup
    # This section is for testing
    if config['debug']:
        import RPi.GPIO as GPIO

        debug_pin = config['debug_pin']
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(debug_pin, GPIO.OUT)
        GPIO.output(debug_pin, GPIO.LOW)

    # Create pipeline 
    logger.info('Creating pipeline.')
    parent_conn, child_conn = Pipe(True)

    #==========================================================================
    # Start another process, which will be calculate data and save it to file
    #==========================================================================
    logger.info('Creating data processer process.')
    data_processor = Process(target=process_data, 
            args=(child_conn, samples, path))
    data_processor.start()

    
    #==========================================================================
    # Run main cycle
    #==========================================================================
    logger.info('Running main cycle.')
    try:
        while True:
            # Debug
            if config['debug']:
                GPIO.output(debug_pin, GPIO.LOW)
                time.sleep(0.0001)
                GPIO.output(debug_pin, GPIO.HIGH)
            # Debug end

            try:
                # Get data from the sensor
                data = parse_data_string(inpoint.read(38))
                parent_conn.send(data)

            except SerialException as e:
                logger.error('Main cycle: Error occured while reading from port.')
                logger.error('Excpetion: ' + str(e))
            
            # Debug
            if config['debug']:
                GPIO.output(debug_pin, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(debug_pin, GPIO.LOW)
            # Debug end

    except KeyboardInterrupt:
        if not virtual:
            inpoint.join()

        logger.info('Exiting.')
        time.sleep(1)
        if config['debug']:
            GPIO.cleanup()
        sys.exit(0)
