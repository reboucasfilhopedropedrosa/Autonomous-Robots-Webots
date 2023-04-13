from vehicle import Driver
from controller import Camera, Lidar
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math


TIME_STEP = 64 # ms
MAX_SPEED = 80 # km/h

driver = Driver()

speed_forward = 10 # km/h
speedBrake = 0 # km/h
cont = 0

cameraRGB = driver.getDevice('camera')
Camera.enable(cameraRGB, TIME_STEP)

lms291 = driver.getDevice('Sick LMS 291')
print(lms291)
Lidar.enable(lms291, TIME_STEP)
lms291_width = Lidar.getHorizontalResolution(lms291)
print(lms291_width)

plot = 10

while driver.step() != -1:
    # # Rotina 1
    # if cont < 1000:
    #     driver.setCruisingSpeed(speed_forward) # acelerador (velocidade)
    #     driver.setSteeringAngle(-0.7) # volante (giro)
    #     # print('speed up %d' % cont)
    #     driver.setDippedBeams(True) # farol ligado
    #     # driver.setIndicator(2) # 0 -> OFF  1 -> Right   2 -> Left
    # elif cont > 1000 and cont < 1100:
    #     driver.setCruisingSpeed(speedBrake)
    #     driver.setBrakeIntensity(1.0) # intensidade (0.0 a 1.0)
    #     driver.setDippedBeams(False) # farol apagado
    #     # print('braked %d' % cont)
    # elif cont > 1100 and cont < 1400:
    #     driver.setCruisingSpeed(-speed_forward)
    #     driver.setSteeringAngle(-0.7)
    #     # print('speed up %d' % cont)
    # elif cont > 1400 and cont < 1500:
    #     driver.setCruisingSpeed(speedBrake)
    #     driver.setBrakeIntensity(1.0)
    #     driver.setDippedBeams(False) # farol apagado
    #     # print('braked %d' % cont)
    # elif cont > 1500:
    #     cont = 0

    # Rotina 2
    if cont < 1000:
        driver.setDippedBeams(True)  # farol ligado
        # driver.setIndicator(0) # 0 -> OFF  1 -> Right   2 -> Left
        driver.setCruisingSpeed(speed_forward)  # acelerador (velocidade)
        driver.setSteeringAngle(0.0)  # volante (giro)
    elif cont > 1000 and cont < 1500:
        driver.setCruisingSpeed(speedBrake)
        driver.setBrakeIntensity(1.0)  # intensidade (0.0 a 1.0)
    elif cont > 1500 and cont < 2500:
        driver.setCruisingSpeed(-speed_forward)  # acelerador (velocidade)
        driver.setSteeringAngle(0.0)  # volante (giro)
    elif cont > 2500:
        cont = 0

    # ler a camera
    Camera.getImage(cameraRGB)
    Camera.saveImage(cameraRGB, 'color.png', 1)
    frameColor = cv2.imread('color.png')
    # dim = (int(frameColor.shape[1] * 3), int(frameColor.shape[0] * 3))
    # resized = cv2.resize(frameColor, dim)
    cv2.imshow('color', frameColor)
    cv2.waitKey(1)

    # Lê o LIDAR
    lms291_values = []
    lms291_values = Lidar.getRangeImage(lms291)

    if plot == 10:
        y = lms291_values
        x = np.linspace(math.pi, 0, np.size(y))
        plt.polar(x, y)
        plt.pause(0.0001)
        plt.clf()
        plot = 0

    plot += 1

    cont += 1