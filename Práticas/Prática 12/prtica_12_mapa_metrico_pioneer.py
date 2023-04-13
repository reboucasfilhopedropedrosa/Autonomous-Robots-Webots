# **************************************************************
# Robótica Móvel IFCE - LAPISCO
# Prof. Dr. Pedro Pedrosa Rebouças Filho
#
# Simulação 13 com robô Pioneer3dx - Webots R2023a
# Mapa métrico
# Python 3.10 na IDE Pycharm - controller <extern>
# 
# Hector Leonardo Mota Moreira
#
# Baseado nos códigos de Jefferson Silva Almeida                     
# **************************************************************

from controller import Robot
from controller import Motor
from controller import PositionSensor
import math

TIME_STEP = 64
MAX_SPEED = 1.2

robot = Robot()

positionLeft = robot.getPositionSensor('left wheel sensor')
positionRight = robot.getPositionSensor('right wheel sensor')
PositionSensor.enable(positionLeft, TIME_STEP)
PositionSensor.enable(positionRight, TIME_STEP)

leftMotor = robot.getDevice('left wheel')
rightMotor = robot.getDevice('right wheel')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

leftMotor.setVelocity(0.5 * MAX_SPEED)
rightMotor.setVelocity(0.5 * MAX_SPEED)

diametroRoda = 0.195  # metro
raioRoda = diametroRoda / 2
comprimentoRoda = 2 * math.pi * raioRoda

while robot.step(TIME_STEP) != -1:
    encoderLeft = PositionSensor.getValue(positionLeft) / 10
    encoderRight = PositionSensor.getValue(positionRight) / 10

    print('encoders: Left= %f m Right= %f m' % (encoderLeft, encoderRight))