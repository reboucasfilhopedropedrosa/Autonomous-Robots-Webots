# **************************************************************
# Robótica Móvel IFCE - LAPISCO
# Prof. Dr. Pedro Pedrosa Rebouças Filho
#
# Simulação 06 com robô Pioneer 3AT - Webots R2023a
# Kinect - Detecção de círculos
# Python 3.10 na IDE Pycharm - controller <extern>
# 
# Hector Leonardo Mota Moreira
#
# Baseado nos códigos de Jefferson Silva Almeida                     
# **************************************************************

from controller import Robot
from controller import Motor
from controller import DistanceSensor
from controller import Camera
from controller import RangeFinder
import cv2 as cv
import numpy as np

# time in [ms] of a simulation step
TIME_STEP = 64

MAX_SPEED = 6.28

# maximal value returned by the sensors
MAX_SENSOR_VALUE = 1024
# minimal distance, in meters, for an obstacle to be considered
MIN_DISTANCE = 1.0

# create the robot instance
robot = Robot()

# inicializa kinect
kinectColor = robot.getDevice('kinect color')
kinectDepth = robot.getDevice('kinect range')
print(kinectColor)
Camera.enable(kinectColor, TIME_STEP)
RangeFinder.enable(kinectDepth, TIME_STEP)

# get a handler to the motors and set target position to infinity (speed control)
leftMotorFront = robot.getDevice('front left wheel')
rightMotorFront = robot.getDevice('front right wheel')
leftMotorBack = robot.getDevice('back left wheel')
rightMotorBack = robot.getDevice('back right wheel')

leftMotorFront.setPosition(float('inf'))
rightMotorFront.setPosition(float('inf'))
leftMotorBack.setPosition(float('inf'))
rightMotorBack.setPosition(float('inf'))

# initialize devices
ps = []
psNames = [
    'so0', 'so1', 'so2', 'so3',
    'so4', 'so5', 'so6', 'so7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)

ball = 0
# cont = 0
while robot.step(TIME_STEP) != -1:
    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
        # print(psValues[i])

    # detect obstacles
    right_obstacle = psValues[0] > 50.0 or psValues[1] > 50.0 or psValues[2] > 50.0
    left_obstacle = psValues[5] > 50.0 or psValues[6] > 50.0 or psValues[7] > 50.0
    front_obstacle = psValues[3] > 50.0 or psValues[4] > 50.0
    # print(right_obstacle)
    # print(left_obstacle)

    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed = 0.7 * MAX_SPEED
    rightSpeed = 0.7 * MAX_SPEED

    # modify speeds according to obstacles
    if front_obstacle:
        leftSpeed = -0.5 * MAX_SPEED
        rightSpeed = +0.5 * MAX_SPEED
    elif left_obstacle:
        leftSpeed = -0.5 * MAX_SPEED
        rightSpeed = +0.5 * MAX_SPEED
    elif right_obstacle:
        leftSpeed = +0.5 * MAX_SPEED
        rightSpeed = -0.5 * MAX_SPEED

    # set up the motor speeds at x% of the MAX_SPEED.
    leftMotorFront.setVelocity(leftSpeed)
    rightMotorFront.setVelocity(rightSpeed)
    leftMotorBack.setVelocity(leftSpeed)
    rightMotorBack.setVelocity(rightSpeed)

    Camera.getImage(kinectColor)
    Camera.saveImage(kinectColor, 'color.png', 1)
    # file = '/home/jefferson/PycharmProjects/webotsTeste07/imagens/color' + str(cont) + '.png'
    # Camera.saveImage(kinectColor, file, 1)
    # cont += 1

    frameColor = cv.imread('color.png')

    # detect circles with opencv
    output = frameColor.copy()
    gray = cv.cvtColor(frameColor, cv.COLOR_BGR2GRAY)
    gray_blurred = cv.blur(gray, (3, 3))
    circles = cv.HoughCircles(gray_blurred, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=40)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv.circle(output, (x, y), r, (0, 255, 0), 4)
            cv.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            ball = 1

    if ball == 1:
        print("Bola detectada!")

    cv.imshow("Color", output)
    cv.waitKey(10)