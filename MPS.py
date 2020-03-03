#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

# Encoder and functions

import time
import os
import numpy
import spidev

# Enable SPI
spi = spidev.SpiDev()


class MPS_Encoder(object):

    def __init__(self, name, chip_bus, cs, max_speed, mode):
        self.name = name
        self.chip_bus = chip_bus
        self.cs = cs
        self.max_speed = max_speed
        self.mode = mode

    def connect(self):
        # Open a connection to a specific bus and device (chip select pin)
        spi.open(self.chip_bus, self.cs)
        # Set SPI speed and mode
        spi.max_speed_hz = self.max_speed
        spi.mode = self.mode
        print("Device connected.")

    
    def read_angle(self):
        # Read angle from device
        data = spi.readbytes(2)
        high_byte = data[0] << 8
        low_byte = (data[1] >> 4) << 4  # Get rid of last 4 bit whatever
        angle = high_byte + low_byte
        return angle

    def release(self):
        # Disconnect the device
        spi.close()
        print("Device released.")

# bi_angle = bin(angle[0])<<8
# print(bi_angle)
# bi_angle = [bin(angle[0])]
# bangle.append(bin(angle[1]))
# print(angle)
# print(bangle)
# time.sleep(0.001)
