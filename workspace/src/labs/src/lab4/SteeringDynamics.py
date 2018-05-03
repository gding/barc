#!/usr/bin/env python

# ---------------------------------------------------------------------------
# Licensing Information: You are free to use or extend these projects for
# education or reserach purposes provided that (1) you retain this notice
# and (2) you provide clear attribution to UC Berkeley, including a link
# to http://barc-project.com
#
# Attibution Information: The barc project ROS code-base was developed at UC
# Berkeley in the Model Predictive Control (MPC) lab by Jon Gonzales
# (jon.gonzales@berkeley.edu) and Greg Marcil (grmarcil@berkeley.edu). The cloud
# services integation with ROS was developed by Kiet Lam
# (kiet.lam@berkeley.edu). The web-server app Dator was based on an open source
# project by Bruce Wootton
# ---------------------------------------------------------------------------

# README: This node serves as an outgoing messaging bus from odroid to arduino
# Subscribes: steering and motor commands on 'ecu'
# Publishes: combined ecu commands as 'ecu_pwm'

from rospy import init_node, Subscriber, Publisher, get_param
from rospy import Rate, is_shutdown, ROSInterruptException, spin, on_shutdown
from barc.msg import ECU
from numpy import pi
import rospy
import time

motor_pwm = 1500
servo_pwm = 1600

def arduino_interface():
    global ecu_pub, motor_pwm, servo_pwm

    init_node('arduino_interface')
    # set node rate
    loop_rate   = 50
    dt          = 1.0 / loop_rate
    rate        = rospy.Rate(loop_rate)

    time_prev = time.time()
    ecu_pub = Publisher('ecu_pwm', ECU, queue_size = 10)

    motor_pwm = 1600
    servo_pwm = 1600
    flag = 0
    x0 = 12
    x1 = x0 + 1
    x2 = x1 + 2
    x3 = x2 + 1
    x4 = x3 + 2
    x5 = x4 + 1
    x6 = x5 + 2
    x7 = x6 + 1
    x8 = x7 + 7
    x9 = x8 + 1
    x10 = x9 + 7
    x11 = x10 + 1
    x12 = x11 + 2
    x13 = x12 + 1
    x14 = x13 + 2
    x15 = x14 + 1
    x16 = x15 + 2
    x17 = x16 + 1
    x18 = x17 + 8
    while not rospy.is_shutdown():
        if time.time() - time_prev < x0:
            servo_pwm = 1530
        elif time.time() - time_prev < x1: #1
            servo_pwm = 1650
        elif time.time() - time_prev < x2: #2
            servo_pwm = 1530
        elif time.time() - time_prev < x3: #3
            servo_pwm = 1670
        elif time.time() - time_prev < x4: #4
            servo_pwm = 1530
        elif time.time() - time_prev < x5: #5
            servo_pwm = 1670
        elif time.time() - time_prev < x6: #6
            servo_pwm = 1530
        elif time.time() - time_prev < x7: #7
            servo_pwm = 1640
        elif time.time() - time_prev < x8: #8
            servo_pwm = 1530
        elif time.time() - time_prev < x9: #9
            servo_pwm = 1680
        elif time.time() - time_prev < x10: #10
            servo_pwm = 1530
        elif time.time() - time_prev < x11: #11
            servo_pwm = 1630
        elif time.time() - time_prev < x12: #12
            servo_pwm = 1530
        elif time.time() - time_prev < x13: #13
            servo_pwm = 1650
        elif time.time() - time_prev < x14: #14
            servo_pwm = 1530
        elif time.time() - time_prev < x15: #15
            servo_pwm = 1650
        elif time.time() - time_prev < x16: #16
            servo_pwm = 1530
        elif time.time() - time_prev < x17: #17
            servo_pwm = 1650
        elif time.time() - time_prev < x18: #18
            servo_pwm = 1580

        ecu_cmd = ECU(motor_pwm, servo_pwm)
        ecu_pub.publish(ecu_cmd)

        #wait
        rate.sleep()
    # while not rospy.is_shutdown():
    #
    #     if time.time()-time_prev>=12:
    #         servo_pwm = 1600; #reset to straight ahead
    #         ecu_cmd = ECU(motor_pwm, servo_pwm)
    #         ecu_pub.publish(ecu_cmd)
    #         break
    #     elif time.time()-time_prev >=7:
    #         servo_pwm = 1625; #send new steering angle command: [1450, 1500, 1575, 1625, 1700,1750]
    #
    #
    #     ecu_cmd = ECU(motor_pwm, servo_pwm)
    #     ecu_pub.publish(ecu_cmd)
    #
    #     # wait
    #     rate.sleep()

#############################################################
if __name__ == '__main__':
    try:
        arduino_interface()
    except ROSInterruptException:
        pass
