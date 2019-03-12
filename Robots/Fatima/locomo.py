#Este script solo recibira las ordenes mandadas desde el pc por socket.
#no se tendra acceso al radar ni al imu.

import sys
import time
import socket
import RPi.GPIO as GPIO

HOST = '192.168.25.113' #IP DE LA RASPBERRY
PORT = 65435

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()

GPIO.setmode (GPIO.BCM)
motorA1=4 #out1 in1 
motorA2=23 #out1 in3 
motorB1=17 #out2 in2 
motorB2=22 #out2 in4 
motorena=18
motorenb=26
GPIO.setwarnings(False)
GPIO.setup(motorA1,GPIO.OUT)
GPIO.setup(motorA2,GPIO.OUT)
GPIO.setup(motorB1,GPIO.OUT)
GPIO.setup(motorB2,GPIO.OUT)
GPIO.setup(motorena,GPIO.OUT)
GPIO.setup(motorenb,GPIO.OUT)

ena=GPIO.PWM(motorena,500)
enb=GPIO.PWM(motorenb,500)
ena.start(0)
enb.start(0)

def adelante():
#    print "adelante"
    ena.ChangeDutyCycle(100) #duty cycle(40,40)
    enb.ChangeDutyCycle(100)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.HIGH)

def izquierda():
 #   print "izquierda"
    #duty cycle
    ena.ChangeDutyCycle(90)
    enb.ChangeDutyCycle(0)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.LOW)

def spinizq():
#    print "izquierda(spin)"
    #duty cycle
    ena.ChangeDutyCycle(100)
    enb.ChangeDutyCycle(100)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.HIGH)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.LOW)


def derecha():
#    print "derecha"
    #duty cycle
    enb.ChangeDutyCycle(100)
    ena.ChangeDutyCycle(0)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB2,GPIO.HIGH)

def spinder():
#    print "derecha(spin)"
    #duty cycle
    enb.ChangeDutyCycle(100)
    ena.ChangeDutyCycle(100)
    GPIO.output(motorA1,GPIO.HIGH)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB2,GPIO.HIGH)


def detenerse():
#    print "detenerse"
    #duty cycle
    ena.ChangeDutyCycle(0)
    enb.ChangeDutyCycle(0)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)


def mov():
    data = conn.recv(1024)
    if not data:
        return 0
    else:
        return 1
    # ANALISIS DE DATA
    cmdRaw = data.partition('s') # Separa la trama al encontrar el caracter s (cmd,s,'')
    cmd= cmdRaw[0] # (cmd)
    # envase al comando realizar un movimiento
    if (cmd == 'w'):
        adelante()
    if (cmd == 'a'):
        izquierda()
    if (cmd == 'd'):
        derecha()
    if (cmd == 'q'):
        spinizq()
    if (cmd == 'e'):
        spinder()
    if (cmd == 'x'):
        print("Modulos Desactivados")
        conn.close()
        time.sleep(2)
        GPIO.cleanup()
        sys.exit()
    else:
        detenerse() #se enviara una z indicando que el boton ha sido soltado.


