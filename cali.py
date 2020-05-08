#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

# Encoder calibration related functions

from MPS import *
from motor_controller import *

# We only have SPI bus 0 available to us on the Pi
bus = 0
# Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 0
max_speed_hz = 2000
spi_mode = 0
bear_baudrate = 8000000
bear_port = "/dev/ttyUSB0"


class cali(object):
    MA310 = MPS_Encoder("cali.MA310", bus, device, max_speed_hz, spi_mode)
    MC = MotorController(bear_baudrate, bear_port)

    def __init__(self, m_id, data_count):
        self.m_id = m_id
        self.data_count = data_count

    def BEAR_Initialization(self, m_id):
        # Initialize the BEAR with ID = m_id for the calibration process

        # 1. Clear HOMING_OFFSET
        cali.MC.pbm.set_homing_offset((m_id, 0))
        # Check setting
        check = False
        trial_count = 1
        while not check:
            try:
                if abs(cali.MC.pbm.get_homing_offset(m_id)[0]) < 1:
                    check = True
                    print("HOMING_OFFSET cleared. Trails: %d." % trial_count)
                else:
                    cali.MC.pbm.set_homing_offset((m_id, 0))
                    time.sleep(0.05)
                    trial_count += 1
            except KeyboardInterrupt:
                check = True
                print("User interrupted.")
        # Wait for 1 sec after setting HOMING_OFFSET
        time.sleep(1)

        # 2. Restore position limit to default
        cali.MC.pbm.set_limit_position_min((m_id, -131072))
        cali.MC.pbm.set_limit_position_max((m_id, 131072))

        # 3. Set limits, PID and operation mode
        # Set Limits
        cali.MC.pbm.set_limit_iq_max((m_id, 4))
        cali.MC.pbm.set_limit_velocity_max((m_id, 100))

        # Set PID Gains
        # Velocity
        cali.MC.pbm.set_p_gain_velocity((m_id, 0.1))
        cali.MC.pbm.set_i_gain_velocity((m_id, 0.0005))
        # Position
        cali.MC.pbm.set_p_gain_position((m_id, 0.003))
        cali.MC.pbm.set_d_gain_position((m_id, 0.001))

        # Set mode
        cali.MC.set_mode(m_id, 'position')

        # 4. Save
        cali.MC.pbm.save_config(m_id)
        
    def MPS_Initialization(self, m_id):
        # Connect encoder
        cali.MA310.connect()
        # Move BEAR to 0
        cali.MC.torque_enable(m_id, 1)
        cali.MC.pbm.set_goal_position((m_id, 0))
        # Home MA310
        check = cali.MA310.home()
        # Release the devices
        cali.MC.torque_enable(m_id, 0)
        cali.MA310.release()
        if check:
            print("MPS homed with BEAR zero.")
        else:
            print("MPS initialization failed.")
        return check
            

    def record(self, m_id, data_count, filename):
        # Record n calibration data with BEAR ID = m_id
        # The calibration process goes a full 360
        n = data_count
        # 1. Connect encoder
        cali.MA310.connect()
        # 2. Generate trajectory
        # Only need step length here
        step = 262144 // n
        start = -131072 + step // 2

        # 3. Move and read
        cali.MC.torque_enable(m_id, 1)
        # Move motor from min_Pos-step/2 and record
        # BEAR range: -131072 ~ 131071
        cali.MC.pbm.set_goal_position((m_id, 0))
        time.sleep(1)
        cali.MC.pbm.set_goal_position((m_id, start))
        time.sleep(2)
        print("BEAR at start pos.")
        # Initialize position lists
        BEAR_Pos = [0] * n
        Encoder_Pos = [0] * n

        for x in range(n):
            try:
                cali.MC.pbm.set_goal_position((m_id, start + x * step))
                time.sleep(0.5)
                BEAR_Pos[x] = cali.MC.pbm.get_present_position(m_id)[0]
                Encoder_Pos[x] = cali.MA310.read_angle()
                print(x)

            except KeyboardInterrupt:
                check = True
                print("User interrupted.")

        # 4. Release the device
        cali.MC.torque_enable(m_id, 0)
        cali.MA310.release()

        # print(BEAR_Pos,'\n',Encoder_Pos)

        # 5. Write data into file
        # Write file
        # filename = 'calibration_record.txt'
        print(os.getcwd())
        filepath = os.path.join(os.getcwd(), filename)
        print(filepath)
        records = open(filepath, 'w')
        for x in range(n):
            records.write('%d,%d\n' % (BEAR_Pos[x], Encoder_Pos[x]))
        records.close()
        print('Record written to file.')

# def write_BTC(BTC):
#     cali.MA310.connect()
#     check = cali.MA310.write_BTC(BTC)
#     if check:
#         print("BTC updated.")
#     else:
#         print("Failed to update BTC.")
#     cali.MA310.release()
#     return check
#
# def read_BTC():
#     cali.MA310.connect()
#     BTC = cali.MA310.read_BCT()
#     cali.MA310.release()
#     return BTC


# if __name__ == '__main__':
#     motor_id = 1
#     step_count = 360
#     user = input("Is this a BTC test?(y/n)")
#     if user == 'n':
#         BTC_inchip = read_BTC()
#         if BTC_inchip != 0:
#             write_BTC(0)
#     else:
#         BTC = int(round(float(input("Please input BTC:\n"))))
#         BTC_inchip = read_BTC()
#         if BTC != BTC_inchip:
#             write_BTC(BTC)
#
#     BEAR_Initialization(motor_id)
#     record(motor_id, step_count)
