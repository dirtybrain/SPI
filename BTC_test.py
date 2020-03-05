#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

# Use this code to write BTC to encoder

import time
import os
import numpy
from MPS import *
import cali

BTC = 180
BTC_inchip = cali.read_BTC()