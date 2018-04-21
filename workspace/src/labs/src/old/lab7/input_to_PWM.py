#!/usr/bin/env python

# Author: Tony Zheng
# MEC231A BARC Project 

import rospy
import time
from geometry_msgs.msg import Twist
from barc.msg import ECU, Input, Moving

def enc_callback(data):
    global t0, v_meas
    global n_FL, n_FR, n_BL, n_BR
    global ang_km1, ang_km2

    n_FL = data.FL
    n_FR = data.FR
    n_BL = data.BL
    n_BR = data.BR

    # compute the average encoder measurement
    n_mean = (n_FL + n_FR)/2

    # transfer the encoder measurement to angular displacement
    ang_mean = n_mean*2*pi/8

    # compute time elapsed
    tf = time.time()
    dt = tf - t0
    
    # compute speed with second-order, backwards-finite-difference estimate
    v_meas    = 0.05*(ang_mean - 4*ang_km1 + 3*ang_km2)/(dt)
    rospy.logwarn("velocity = {}".format(v_meas))
    # update old data
    ang_km1 = ang_mean
    ang_km2 = ang_km1
    t0      = time.time()

    v_ref = 0.5

def start_callback(data):
    global move, still_moving
    #print("2")
    #print(move)
    if data.linear.x >0:
        move = True
    elif data.linear.x <0:
        move = False
    #print("3")
    #print(move)

def moving_callback_function(data):
    global still_moving, move
    if data.moving == True:
        still_moving = True
    else:
        move = False
        still_moving = False

# update
def callback_function(data):
    global move, still_moving
    ################################################################################################################################################
    # Convert the velocity into motorPWM and steering angle into servoPWM
    v_ref = data.vel
    s_ref = data.delta
    newECU.motor = (0.0139/0.7910)*v_ref + 1500 
    newECU.servo = (-s_ref*180)/(1.846*3.1415926535) + 283.5157/1.846
    #################################################################################################################################################

    maxspeed = 1568
    minspeed = 1400
    servomax = 1800
    servomin = 1200
    if (newECU.motor<minspeed):
        newECU.motor = minspeed
    elif (newECU.motor>maxspeed):
        newECU.motor = maxspeed
    if (newECU.servo<servomin):
        newECU.servo = servomin
    elif (newECU.servo>servomax):
        newECU.servo = servomax     # input steering angle

    #print("5")
    #print(move)

class PID():
    def __init__(self, kp=1, ki=1, kd=1, integrator=0, derivator=0):
        self.kp = kp
        self.ki = ki
        self.integrator = integrator
        self.integrator_max = 100

    def acc_calculate(self, speed_reference, speed_current):
        self.error = speed_reference - speed_current
        
        # Propotional control
        self.P_effect = self.kp*self.error
        
        # Integral control
        self.integrator = self.integrator + self.error
        
		# Anti windup
        if self.integrator >= self.integrator_max:
           self.integrator = self.integrator_max

        self.I_effect = self.ki*self.integrator

        acc = self.P_effect + self.I_effect

        return acc

# state estimation node
def inputToPWM():
    
    # initialize node
    rospy.init_node('inputToPWM', anonymous=True)
    
    global pubname , newECU , subname, move , still_moving
    newECU = ECU() 
    newECU.motor = 1500
    newECU.servo = 1550
    move = False
    still_moving = False
    #print("1")
    #print(move)
    # topic subscriptions / publications
    pubname = rospy.Publisher('ecu_pwm',ECU, queue_size = 2)
    rospy.Subscriber('turtle1/cmd_vel', Twist, start_callback)
    subname = rospy.Subscriber('uOpt', Input, callback_function)
    rospy.Subscriber('moving', Moving, moving_callback_function)
    # set node rate
    loop_rate   = 40
    ts          = 1.0 / loop_rate
    rate        = rospy.Rate(loop_rate)
    t0          = time.time()
    PID_control = PID(kp=20,ki=5,kd=0.0)
    v_ref = 0.5
    v_meas = 0.0
    motor_pwm_offset = 1500
     
    while not rospy.is_shutdown():
      motor_pwm = PID_control.acc_calculate(v_ref,v_meas) + motor_pwm_offset
      newECU.motor = motor_pwm
      if ((move == False) or (still_moving == False)):
        newECU.motor = 1500;
        newECU.servo = 1540;
      pubname.publish(newECU)

      rate.sleep()

if __name__ == '__main__':
    try:
       inputToPWM()
    except rospy.ROSInterruptException:
        pass
