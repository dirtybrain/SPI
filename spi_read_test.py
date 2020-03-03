#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

import time
import os
import numpy
import spidev

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 0

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 2000
spi.mode = 0

read = spi.readbytes(2)
high_byte = read[0]<<8
low_byte = (read[1]>>4)<<4 # Get rid of last 4 bit whatever
angle = high_byte+low_byte
print(angle)

#bi_angle = bin(angle[0])<<8
#print(bi_angle)
#bi_angle = [bin(angle[0])]
#bangle.append(bin(angle[1]))
#print(angle)
#print(bangle)
#time.sleep(0.001)

