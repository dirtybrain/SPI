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
from MPS_CONTROL_TABLE import *

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
        low_byte = data[1]
        angle = (high_byte + low_byte) >> 4  # Get rid of last 4 bit whatever
        return angle

    def read_BCT(self):
        # Read the BCT register value
        send = 0b01000010
        spi.writebytes([send, 0])
        data = spi.readbytes(2)
        BTC = data[0]
        return BTC

    def write_BTC(self, BTC):
        # Write the BCT register value
        # BTC value
        send = 0b10000010
        spi.writebytes([send, BTC])
        time.sleep(0.02)
        data = spi.readbytes(2)
        high_byte = data[0]
        if high_byte == BTC:
            return True
        else:
            return False

    def release(self):
        # Disconnect the device
        spi.close()
        print("Device released.")

    def read_reg(self, reg_name):
        # Read from a register
        packet = INSTRUCTION.read + REG_DIC[reg_name]
        spi.writebytes([packet, 0])
        data = spi.readbytes(2)
        reg_val = data[0]
        return reg_val

    def write_reg(self, reg_name, reg_val):
        # Write to a register
        packet = INSTRUCTION.write + REG_DIC[reg_name]
        spi.writebytes([packet, reg_val])
        time.sleep(0.02)
        data = spi.readbytes(2)
        return_val = data[0]
        if return_val == reg_val:
            return True
        else:
            return False
