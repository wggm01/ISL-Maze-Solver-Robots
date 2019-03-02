# instalar pip install mpu9250 https://github.com/MomsFriendlyRobotCompany/mpu9250
# pip install FaBo9Axis_MPU9250 https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python

import RPi.GPIO as GPIO
import time
import FaBo9Axis_MPU9250
import sys
import math

GPIO.setmode(GPIO.BCM)
TRIG = 6
ECHO = 5
SERVO= 13
timeout=[0]
pulse=[0,0]

GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(SERVO,GPIO.OUT)
SRV=GPIO.PWM(SERVO,50)
SRV.start(0)

RAD_TO_DEG = 57.295779513082320876798154814105 #valor para realizar conversiones de radianes a grados
#variables para realizar el calculo de angulos de euler
grxyz=[0,0,0]#gyroRatex,gyroRatey,gyroRatez;
gpry = [0,0,0] #gpitch,groll,gyaw;
arxyz=[0,0,0]#accRatex,accRatey,accRatez;
accpr=[0,0]#accpitch,accroll;
pry=[0,0,0]#pitch,roll,yaw;
#variables para realizar el calculo de angulos de euler
theta=[0]
lastdeg=[0]
#mpu9250 = FaBo9Axis_MPU9250.MPU9250()

def deg(theta):
    dc=0.04722222222*theta+2.5
    dc=round(dc,2)
    if (lastdeg[0]==dc):
        pass
    else:
        #print(dc)
        SRV.ChangeDutyCycle(dc)
        lastdeg[0]=dc
    if (theta==180):
        return 1
    else:
        return 0
        
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
    GPIO.output(TRIG, False)
    time.sleep(0.0050/1000)
    #gap entre mediciones
    GPIO.output(TRIG, True)
    time.sleep(0.0100/1000)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 0:
        pulse[0] = time.time()
    while GPIO.input(ECHO) == 1:
        pulse[1] = time.time()
    pulse_duration = pulse[1] - pulse[0]
    
    distance = pulse_duration*17150
    distance = round(distance, 2)
    return distance
    

try:
  while True:
    for ccw in range(1,180):
        idle=deg(ccw)
        r=hcsr04()
        print(r)
        time.sleep(0.080)
    for cw in range(180,1,-1):
        idle=deg(cw)
        
        time.sleep(0.080)

except KeyboardInterrupt:
  SRV.stop()
  GPIO.cleanup()
#try:
#    while True:
        #accel = mpu9250.readAccel()
        #print " ax = " , ( accel['x'] )
        #print " ay = " , ( accel['y'] )
        #print " az = " , ( accel['z'] )

        #gyro = mpu9250.readGyro()
        #print " gx = " , ( gyro['x'] )
        #print " gy = " , ( gyro['y'] )
        #print " gz = " , ( gyro['z'] )
#        hcsr04()
#        time.sleep(0.5)

#except KeyboardInterrupt:
#    sys.exit()
