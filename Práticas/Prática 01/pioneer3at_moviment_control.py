# **************************************************************
# Robótica Móvel IFCE - LAPISCO
# Prof. Dr. Pedro Pedrosa Rebouças Filho
#
# Simulação 01 com robô Pioneer 3AT - Webots R2023a
# Acionamento dos motores
# Python 3.10 na IDE Pycharm - controller <extern>
# 
# Hector Leonardo Mota Moreira
#
# Baseado nos códigos de Jefferson Silva Almeida                     
# **************************************************************

from controller import Robot
from controller import Motor

TIME_STEP = 64
MAX_SPEED = 6.28

# create the robot instance
robot = Robot()

# get a handler to the motors and set target position to infinity (speed control)
leftMotorFront = robot.getDevice('front left wheel')
rightMotorFront = robot.getDevice('front right wheel')
leftMotorBack = robot.getDevice('back left wheel')
rightMotorBack = robot.getDevice('back right wheel')

leftMotorFront.setPosition(float('inf'))
rightMotorFront.setPosition(float('inf'))
leftMotorBack.setPosition(float('inf'))
rightMotorBack.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
leftMotorFront.setVelocity(0.3 * MAX_SPEED)
rightMotorFront.setVelocity(0.3 * MAX_SPEED)
leftMotorBack.setVelocity(0.3 * MAX_SPEED)
rightMotorBack.setVelocity(0.3 * MAX_SPEED)


while robot.step(TIME_STEP) != -1:
    pass
