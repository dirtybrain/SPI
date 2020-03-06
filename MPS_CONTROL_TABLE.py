#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

"""
Register Table
"""


class INSTRUCTION:
    """MPS Instruction"""
    read = 0b01000000
    write = 0b10000000


class REG:
    """MPS Registers"""
    BCT = 0x02
    Sensor_Orientation = 0x03


REG_DIC = {'BTC': REG.BCT,
           'sensor_orientation': REG.Sensor_Orientation}
