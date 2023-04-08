import KeyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math

######## PARAMETERS ###########

drone_fSpeed = 15  # Forward Speed in cm/s   (15cm/s)

drone_aSpeed = 36  # Angular Speed Degrees/s  (36d/s)

interval = 0.25

dInterval = drone_fSpeed * interval

aInterval = drone_aSpeed * interval

###############################################

x, y, z = 500, 500, 100

a = 0

yaw = 0

kp.init()

#me = drone()
# me.connect()
# print(me.get_battery())

points = []


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 15

    aspeed = 36

    global x, y, z, yaw, a

    d = 0

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
        z += dInterval

    elif kp.getKey("s"):
        ud = -speed
        z -= dInterval

    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

    # if kp.getKey("q"):
    # #    me.land()
    #     sleep(3)

    # if kp.getKey("e"):;
    # #    me.takeoff()

    sleep(interval)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y, z]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, (point[0], point[1]), 2, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, (points[-1][0], points[-1][1]), 5, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100}, {(points[-1][2]) / 100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


while True:

    vals = getKeyboardInput()

    #me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)

    points.append((vals[4], vals[5], vals[6]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
    if kp.getKey("q"):
        break
