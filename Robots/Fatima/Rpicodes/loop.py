#PROGRAMA ENCARGADO DE EJECUTAR SCRIPT PRINCIPAL DE TRABAJO.
import RPi.GPIO as GPIO
import sys
import time
import os
GPIO.setmode (GPIO.BCM) #nomenclatura GPIO# no numero de pin
ledS=19 #led  de estado de espera/eleccion de modo
b1=25 #boton para prender arduino/MODO MANUAL(activacion en lectura de cero)
flag=0
GPIO.setwarnings(False)
GPIO.setup(ledS,GPIO.OUT)
GPIO.setup(b1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #la raspberry actuara cuando reciba 3.3v

while (flag == 0):
        print ("wating")
        GPIO.output(ledS,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(ledS,GPIO.LOW)
        
        b1S=GPIO.input(b1)
        time.sleep(0.5)
        if (b1S==1): #se sale si presionas b1
            flag=1
            break


os.system('python rpiard.py')
time.sleep(1)
sys.exit()
