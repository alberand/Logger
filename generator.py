#!/usr/bin/python
# coding=utf-8

# System imports
import random

class Generator:
    """
    This class is used only in 'Virtual' mode. In this mode we are don't have
    connected sensor and just generate random values for test program. So this
    class implements basic function of serial port.
    """

    def __init__(self):
        pass

    def write(self, data):
        """
        Just print received data.

        Args:
            data: string
        """
        print('Generator. Received data: ' + str(data))

    def read(self, number_of_byte):
        """
        This function return string in this format:
        1234567;1234567;1234567;1234567;
        Numbers are just random.

        Args:
            number_of_byte: not used
        Returns:
            string
        """
        data = [self.__randint() for i in range(4)]
        return '+{0};+{1};+{2};+{3};'.format(*data)

    def readline(self):
        """
        This function return string in this format:
        1234567;1234567;1234567;1234567;
        Numbers are just random.

        Returns:
            string
        """
        data = [self.__randint() for i in range(4)]
        return '+{0};+{1};+{2};+{3};'.format(*data)

    def __randint(self):
        '''
        Return a 7 number long number.

        Returns:
            int
        '''
        return random.randint(1000000, 9999999)

if __name__ == '__main__':
    """
    Testing section.
    Run this file as a main file to run this section.
        python generator.py
    """
    a = Generator()
    print(a.readline())
