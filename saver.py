#!/usr/bin/python
# coding=utf-8

# System imports
import sys
import time
import queue
import socket
import select
import datetime
import threading as th
import logging.config

#==============================================================================
# In this file we have a few function which are running in one process but in a
# different thread. First of all we run 'data_saver' which save data to file.
# This function run another thread with target function 'sendToSocket' which
# send data to socket.
#==============================================================================

# Local imports
from calibration import save_data

def data_saver(pipeline, path='./'):
    '''
    This function is run as a process and its save data getted from pipeline.

    Args:
        pipeline: pipeline
        path: path where to save data
    '''
    logger = logging.getLogger(__name__)

    # Queue between threads
    d_queue = queue.Queue(maxsize=10)

    # Start thread which will send data to socket.
    socket_th = SocketCommunication(d_queue)
    socket_th.start()

    try:
        while True:
            data = list()
            # Get data
            data.append(pipeline.recv())

            if not d_queue.full():
                d_queue.put(data)
                
            logger.info('Save calibrated data.')
            save_data(data, path=path, suffix='result')

    except KeyboardInterrupt:
        logger.info('Keyboard interrupt in process \'saver\'.')
        socket_th.stop()
        socket_th.join()
        sys.exit(0)

class SocketCommunication(th.Thread):

    def __init__(self, queue):
        th.Thread.__init__(self)
        self.queue = queue

        self.running = True

    def initSocket(self, port):
        """
        Open socket on localhost:port.
        Args:
            port: socket port
        """
        # Initialization of socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('localhost', port))
        serversocket.listen(5)

        # Set timeout
        serversocket.setblocking(False)
        serversocket.settimeout(5)

        return serversocket
    

    def run(self):
        try:
            serversocket = self.initSocket(5000)
        except socket.error:
            print('Fail to init socket. Exiting.')
            sys.exit(1)
    
        while self.running:
            # Wait for some client. 
            try:
                (clientsocket, address) = serversocket.accept()
            except socket.timeout:
                continue
    
            # Run loop with data sending
            while self.running:
                msg = None
                try:
                    # Wait untill user input some symbol or timeout is exceded.
                    ready = select.select([clientsocket], [], [], 5)
                    if ready[0]:
                        msg = clientsocket.recv(3)

                    if not msg:
                        continue

                    # Parse message from user
                    if str(msg[0]) == '113':
                        break
                    elif msg:
                        print('Connection from', address)
                        # c_time = datetime.datetime.now()
                        # while datetime.datetime.now().microsecond > c_time.microsecond:
                        while True:
                            if not self.queue.empty():
                                data = self.queue.get()
                                break
                            else:
                                continue

                        result = ';'
                        result = result.join(list(map(str, data[0])))

                        print(result)
                        clientsocket.sendall(result.encode('ascii'))
    
                except Exception as e:
                    print('Exception while communication with user.')
                    break
    
            clientsocket.close()

        serversocket.close()

    def stop(self):
        self.running = False
