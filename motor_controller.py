#!usr/bin/env python
__author__ = "X Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics Corp."
__date__ = "Feb 14, 2020"

__version__ = "0.0.1"
__status__ = "Prototype"

'''
This module is used to communicate with the BEAR modules 
'''

from pybear import Manager


class MotorController(object):

    def __init__(self, baudrate, port):
        self.baudrate = baudrate
        self.port = port
        self.pbm = Manager.BEAR(port=self.port, baudrate=self.baudrate)

    def start_driver(self, m_id):
        # Set all gains and limits
        # Current
        self.pbm.set_p_gain_id((m_id, 0.0005))
        self.pbm.set_p_gain_iq((m_id, 0.0005))
        self.pbm.set_i_gain_id((m_id, 0.001))
        self.pbm.set_i_gain_iq((m_id, 0.001))
        self.pbm.set_d_gain_id((m_id, 0.005))
        self.pbm.set_d_gain_iq((m_id, 0.005))

        print("Motor driver started.")

    def set_mode(self, m_id, mode):
        """
        Set the single actuator into a desired mode.

        :param int m_id: Motor ID
        :param str mode:
        """
        if mode == 'position':
            m = 2
        elif mode == 'velocity':
            m = 1
        elif mode == 'torque':
            m = 0
        elif mode == 'force':
            m = 4

        self.pbm.set_mode((m_id, m))

    def torque_enable(self, m_id, val):
        """
        Torque enable.

        :param m_id:
        :param int val: Enable/disable torque. (0: disable, 1: enable)
        """
        self.pbm.set_torque_enable((m_id, val))

    def damping_mode(self, m_id):
        """
        Sets the joints into damping mode by reducing the joint limits to 0.0 so that any position triggers damping mode.
        """
        self.pbm.set_limit_position_max((m_id, 0.0))
        self.pbm.set_limit_position_min((m_id, 0.0))

    def get_present_status(self, m_id):
        """
        Get present position of all fingers
        """
        info = self.pbm.get_bulk_status((m_id, 'present_position', 'present_velocity', 'present_iq'))

        return info
