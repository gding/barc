#!/usr/bin/env python

# Author: Tony Zheng
# MEC231A BARC Project

import rospy
import time
from geometry_msgs.msg import Twist
from barc.msg import ECU, Input, Moving, Encoder
from numpy import pi


# from encoder
v_meas      = 0.0
t0          = time.time()
ang_km1     = 0.0
ang_km2     = 0.0
n_FL        = 0.0
n_FR        = 0.0
n_BL        = 0.0
n_BR        = 0.0
r_tire      = 0.05 # radius of the tire

# pwm cmds
motor_pwm   = 1500.0
motor_pwm_offset = 1500.0


# encoder measurement update
def enc_callback(data):
    global t0, v_meas
    global n_FL, n_FR, n_BL, n_BR
    global ang_km1, ang_km2

    n_FL = data.FL
    n_FR = data.FR
    n_BL = data.BL
    n_BR = data.BR

    # compute the average encoder measurement
<<<<<<< 788354075b30aed3675601a88ef2edc39a62e611
    # n_mean = (n_FL + n_FR)/2
    n_mean = n_FL
=======
    n_mean = (n_FL + n_FR)/2
>>>>>>> old

    # transfer the encoder measurement to angular displacement
    ang_mean = n_mean*2*pi/8

    # compute time elapsed
    tf = time.time()
    dt = tf - t0

    # compute speed with second-order, backwards-finite-difference estimate
    v_meas    = r_tire*(3*ang_mean - 4*ang_km1 + ang_km2)/(2*dt)
    # rospy.logwarn("speed = {}".format(v_meas))

    # update old data
    ang_km2 = ang_km1
    ang_km1 = ang_mean
    t0      = time.time()


def start_callback(data):
    global move, still_moving
    #print("2")
    #print(move)
    if data.linear.x > 0:
        move = True
    elif data.linear.x < 0:
        move = False
    #print("3")
    #print(move)
    pubname.publish(newECU)

def moving_callback_function(data):
    global still_moving, move
    if data.moving == True:
        still_moving = True
    else:
        move = False
        still_moving = False

# update
def callback_function(data):
    global move, still_moving, v_ref, servo_pwm
    v_ref = data.vel
    servo_pwm = (data.delta*180/3.1416-53.6364)/-0.0346

    servomax = 1800
    servomin = 1200
    if (servo_pwm<servomin):
        servo_pwm = servomin
    elif (servo_pwm>servomax):
        servo_pwm = servomax     # input steering angle


class PID():
    def __init__(self, kp=1, ki=1, kd=0, integrator=0, derivator=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integrator = integrator
        self.derivator = derivator
        self.integrator_max = 10
        self.integrator_min = -10

    def acc_calculate(self, speed_reference, speed_current):
        self.error = speed_reference - speed_current
<<<<<<< 788354075b30aed3675601a88ef2edc39a62e611
        print(self.error)
        
=======

>>>>>>> old
        # Propotional control
        self.P_effect = self.kp*self.error

        # Integral control
        self.integrator = self.integrator + self.error
        ## Anti windup
        if self.integrator >= self.integrator_max:
            self.integrator = self.integrator_max
        if self.integrator <= self.integrator_min:
            self.integrator = self.integrator_min
        self.I_effect = self.ki*self.integrator

        # Derivative control
        self.derivator = self.error - self.derivator
        self.D_effect = self.kd*self.derivator
        self.derivator = self.error

        acc = self.P_effect + self.I_effect + self.D_effect

        if acc <= 0:
            acc = 20
        return acc

# state estimation node
def inputToPWM():
    global motor_pwm, servo_pwm, motor_pwm_offset, servo_pwm_offset
    global v_ref, v_meas

    # initialize node
    rospy.init_node('inputToPWM', anonymous=True)

    global pubname , newECU , subname, move , still_moving
    newECU = ECU()
    newECU.motor = 1500
    newECU.servo = 1530
    move = False
    still_moving = False
    #print("1")
    #print(move)
    # topic subscriptions / publications
    pubname = rospy.Publisher('ecu_pwm',ECU, queue_size = 2)
    rospy.Subscriber('turtle1/cmd_vel', Twist, start_callback)
    subname = rospy.Subscriber('uOpt', Input, callback_function)
    rospy.Subscriber('moving', Moving, moving_callback_function)
    rospy.Subscriber('encoder', Encoder, enc_callback)

    # set node rate
    loop_rate   = 40
    ts          = 1.0 / loop_rate
    rate        = rospy.Rate(loop_rate)
    t0          = time.time()

    # Initialize the PID controller
<<<<<<< 788354075b30aed3675601a88ef2edc39a62e611
    longitudinal_control = PID(kp=50, ki=1, kd=1)
=======
    longitudinal_control = PID(kp=70, ki=5, kd=0)
>>>>>>> old
    maxspeed = 1700
    minspeed = 1300

    while not rospy.is_shutdown():
        try:
            # acceleration calculated from PID controller
            motor_pwm = longitudinal_control.acc_calculate(v_ref, v_meas) + motor_pwm_offset
            if (motor_pwm<minspeed):
                motor_pwm = minspeed
            elif (motor_pwm>maxspeed):
                motor_pwm = maxspeed

            if (not(move) or not(still_moving)):
                motor_pwm = 1500
<<<<<<< 788354075b30aed3675601a88ef2edc39a62e611
                servo_pwm = 1540
=======
                servo_pwm = 1530
>>>>>>> old

            # publish information
            pubname.publish( ECU(motor_pwm, servo_pwm) )

            # wait
            rate.sleep()
        except:
            pass



if __name__ == '__main__':
    try:
       inputToPWM()
    except rospy.ROSInterruptException:
        pass
