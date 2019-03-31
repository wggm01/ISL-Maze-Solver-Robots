# instalar pip install mpu9250 https://github.com/MomsFriendlyRobotCompany/mpu9250
# pip install FaBo9Axis_MPU9250 https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
timeout=0
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

import math
RAD_TO_DEG = 57.295779513082320876798154814105 #valor para realizar conversiones de radianes a grados
#variables para realizar el calculo de angulos de euler
grxyz=[0,0,0]#gyroRatex,gyroRatey,gyroRatez;
gpry = [0,0,0] #gpitch,groll,gyaw;
arxyz=[0,0,0]#accRatex,accRatey,accRatez;
accpr=[0,0]#accpitch,accroll;
pry=[0,0,0]#pitch,roll,yaw;
#variables para realizar el calculo de angulos de euler

def imu ():
    #proceso de conversion
    grxyz[0] =1 #lectura de imu
    grxyz[1] =1
    grxyz[2] =1
    gpry[0] += (grxyz[0] / 50) * RAD_TO_DEG
    gpry[1] += (grxyz[1] / 50) * RAD_TO_DEG
    gpry[2] += (grxyz[2] / 50) * RAD_TO_DEG
    arxyz[0] = 1 #lectura de imu
    arxyz[1] = 1
    arxyz[2] = 1
    arxyz[0] = arxyz[0]* 0.10197162129779
    arxyz[1] = arxyz[1]* 0.10197162129779
    arxyz[2] = arxyz[2]* 0.10197162129779
    accpr[0] = math.atan(arxyz[0] / math.sqrt(math.pow(arxyz[1], 2) + math.pow(arxyz[2], 2))) * (RAD_TO_DEG)
    accpr[1] = math.atan(arxyz[1] / math.sqrt(math.pow(arxyz[0], 2) + math.pow(arxyz[2], 2))) * (RAD_TO_DEG)
    # Filtrocomplementario:
    pry[0] = 0.97402 * gpry[0] + accpr[0] * 0.02598
    pry[1] = 0.97402 * gpry[1] + accpr[1] * 0.02598
    pry[2] = gpry[2]
    return (pry[0],pry[1],pry[2])

def hcsr04():
    GPIO.output(TRIG, LOW)
    time.sleep(0.0050/1000)
    #gap entre mediciones
    GPIO.output(TRIG, HIGH)
    time.sleep(0.0100/1000)
    GPIO.output(TRIG, LOW)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        echou = echoS*1000000
        if (echou >2915):
            pulse_duration=4678
            timeout=0
            break
        else:
            timeout=1
            break

    if (timeout==1):
        while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

        pulse_duration = (pulse_end - pulse_start)*1000000

    distance = int(0.01715 * pulse_duration)
    return distance

