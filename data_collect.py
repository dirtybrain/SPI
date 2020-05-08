#!usr/bin/env python
__author__ = "Xiaoguang Zhang"
__email__ = "xzhang@westwoodrobotics.net"
__copyright__ = "Copyright 2020 Westwood Robotics"
__date__ = "Jan 8, 2020"
__version__ = "0.0.1"
__status__ = "Prototype"

from cali import *

motor_id = 1
step_count = 360

CF = cali(motor_id, step_count)
CF.MA310.connect()
BTC_inchip = CF.MA310.read_reg('BTC')

user = input("Is this a BTC test?(y/n)")
if user == 'n':
    BTC = 0
    if BTC_inchip != 0:
        check = CF.MA310.write_reg('BTC', 0)
        if check:
            print("BTC reset!")
        else:
            print("BTC rest failed.")
else:
    BTC = int(round(float(input("Please input BTC:\n"))))
    if BTC != BTC_inchip:
        check = CF.MA310.write_reg('BTC', BTC)
        if check:
            print("BTC updated!")
        else:
            print("BTC update failed.")
    else:
        print("No need to update BTC.")
filename = "BTC_"+str(BTC)+".csv"

CF.BEAR_Initialization(motor_id)
CF.MPS_Initialization(motor_id)
CF.record(motor_id, step_count, filename)

