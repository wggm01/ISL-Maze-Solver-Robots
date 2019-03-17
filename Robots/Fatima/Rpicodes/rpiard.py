
from mazelogic import logic # se encarga de la logica en el modo maze(opcion de debugger usando procesing)
from locomo import mov # se encarga de los movimientos en el modo manual
import RPi.GPIO as GPIO
import sys
import serial
import time
GPIO.setmode (GPIO.BCM) #nomenclatura GPIO# no numero de pin
ledS=19 #led  de estado de espera/eleccion de modo
b1=25 #boton para prender arduino/MODO MANUAL(activacion en lectura de cero)
b2=16 #boton para modo Maze(activacion en lectura de cero)
nmos=12 #abre la compuerta del mosfet(para encender necesita un alto)
GPIO.setwarnings(False)
GPIO.setup(ledS,GPIO.OUT) 
GPIO.setup(nmos,GPIO.OUT) 
GPIO.setup(b1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #la raspberry actuara cuando reciba 3.3v
GPIO.setup(b2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
####INCIALIZACION DE PINES PARA L298N####
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
####INCIALIZACION DE PINES PARA L298N####
###CONTROL DE INCIIALIZACION###
flag=0 #activa la secuencia de activacion y acepta el modo debug
flag1=0 #me ayuda a negar el modo debug solamente
b1F=0 #elige el modo maze
b2F=0 #elige el modo manual
enaS=1 # Flag para correr codigo una sola vez
ena2S=1 #Flag para correr codigo una sola vez
debug =0 #control de modo debug
###CONTROL DE INCIIALIZACION###

###tcp###
imu=[0,0,0] # yaw, pitch, roll
rad=['s',0,0] #'dire','ang','distance'
HOST= '192.168.25.113'
PORT= 65441
###tcp###

######Movimiento de los motores######
def adelante(mode):
    ena.ChangeDutyCycle(90)  # duty cycle
    enb.ChangeDutyCycle(90)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1.5)
        detenerse()


def izquierda(mode):
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    if mode == 1:
        time.sleep(1.5)
        detenerse()


def spinizq(mode):
    ena.ChangeDutyCycle(75)
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.HIGH)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    if mode == 1:
        time.sleep(1.5)
        detenerse()


def derecha(mode):
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1.5)
        detenerse()


def spinder(mode):
    enb.ChangeDutyCycle(75)
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.HIGH)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1.5)
        detenerse()


def detenerse():
    ena.ChangeDutyCycle(0)
    enb.ChangeDutyCycle(0)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
######Movimiento de los motores######

###control manual###
def mov():
    data = conn.recv(1024)
    if not data:
        print("Modulos Desactivados")
        conn.close()
        time.sleep(2)
        GPIO.cleanup()
        sys.exit()

    # ANALISIS DE DATA
    cmdRaw = data.partition('s') # Separa la trama al encontrar el caracter s (cmd,s,'')
    cmd= cmdRaw[0] # (cmd)
    # envase al comando realizar un movimiento
    if (cmd == 'w'):
        adelante(0)
    if (cmd == 'a'):
        izquierda(0)
    if (cmd == 'd'):
        derecha(0)
    if (cmd == 'q'):
        spinizq(0)
    if (cmd == 'e'):
        spinder(0)
    if (cmd == 'x'):
        print("Modulos Desactivados")
        conn.close()
        time.sleep(2)
        GPIO.cleanup()
        sys.exit()
    else:
        detenerse() #se enviara una z indicando que el boton ha sido soltado.
###control manual###

###incio del programa###
GPIO.output(nmos,GPIO.LOW)
time.sleep(2)
GPIO.output(nmos,GPIO.HIGH)
#ardS = serial.Serial("/dev/serial0", baudrate = 115200)
ardS = serial.Serial("/dev/ttyUSB0", baudrate = 115200)

try:
    #Prende Led de estado y espera lectura de boton.
    GPIO.output(ledS,GPIO.HIGH)
    
    time.sleep(0.5)#dejar que actue la raspberry
    while (flag == 0):
        print ("wating")
        b1S=GPIO.input(b1)
        time.sleep(0.5)
        if (b1S==1): #se sale si presionas b1
            flag=1
            break
                
    if (flag == 1): #Proceso de encendido de Arduino
        time.sleep(3) #ajustart a tiempo que demore en incializar arduino
        ardS.write(b"1") #Estas despierto?
        ardS.write(b"s") #Estas despierto?
        time.sleep(0.5)
        ardR=ardS.readline()
        while(ardR != '1'): #persiste hasta obtener el feedback del arduino
            print("wating")
            ardR=ardS.readline() #se sale al recibir el 1 del arduino
            ardR=int(ardR)
            if (ardR== 1):
                print("desperto")
                break
    GPIO.output(ledS,GPIO.LOW)
    #GPIO.output(nmos,GPIO.LOW)
    print("Fin de prueba part1")
    


    time.sleep(0.5) #esperar por cualquier eventualidad
    b1S=GPIO.input(b1) #ALMACENO EL ESTADO inicial
    b2S=GPIO.input(b2) #ALMACENO EL ESTADO inicial

    if (b1S==1 and b2S == 1): #SIN  PRESIONAR ESTA EN ALTO
        print("No puede presionar ambos botones a la vez")
    else:
        while (b1S==0 and b2S == 0):
            print("elija el modo")
            b1S=GPIO.input(b1) #ALMACENO EL ESTADO ACTUAL
            time.sleep(0.5)
            if (b1S == 1):
                b1F=1
                print(b1F)
                break
            b2S=GPIO.input(b2) #ALMACENO EL ESTADO ACTUAL
            time.sleep(0.5)
            if (b2S==1):
                b2F=2
                print(b2F)
                break #SALE DEL WHILE SI ALGUNO DE LOS DOS ES PRESIONADO
####################MODO MAZE###################################
    while b1F == 1: #Modo maze activo
        print("MODO MAZE")
        # control de modo debug:
        while (flag == 1):
            for i in range(2):
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(1)  # parpadea 2 veces indica eleccion de debug o !debug.
                GPIO.output(ledS, GPIO.LOW)
            print("desea activar modo maze con debug o !debug")
            b1S = GPIO.input(b1)  # lectura de estado de botones
            b2S = GPIO.input(b2)
            time.sleep(0.5)
            if (b1S == 1):  # debug
                flag = 0
                debug 1
            ######TCP INICIALIZACION#####
                print("Creando Socket")
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                except socket.error:
                    print('Error Socket')
                    print("Modulos Desactivados")
                    ardS.write(b'E')
                    ardS.write(b's')
                    time.sleep(2)
                    sys.exit()
                s.bind((HOST, PORT))
                s.listen(3)  # Maximo tres clientes
                conn, addr = s.accept()
                print('Connected by', addr)
            ######TCP INICIALIZACION#####
                break
            if (b2S == 1):  # !debug
                flag = 0
                debug =0
                break

        if enaS == 1:  # una sola ejecucion
            enaS = 0
            for i in range(3):  # parpadeo de led de estado 3 veces indica modo maze.
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(ledS, GPIO.LOW)

            if (debug):
                ######ARDUINO ACTIVACION DE SISTEMA#####
                for i in range(0, 1):
                    ardS.write(b'R')  # Activacion de los sensores
                    time.sleep(1)
                    ardS.write(b's')  # fin de mensaje
                    time.sleep(0.5)
                    print("Intentando conectar")
                print("UART establecido")
                ######ARDUINO ACTIVACION DE SISTEMA#####
            else:
                ######ARDUINO ACTIVACION DE SISTEMA#####
                for i in range(0, 1):
                    ardS.write(b'R')  # Activacion de los sensores
                    time.sleep(1)
                    ardS.write(b's')  # fin de mensaje
                    time.sleep(0.5)
                    print("Intentando conectar")
                print("UART establecido")
            ######ARDUINO ACTIVACION DE SISTEMA#####

        ###ANALISIS DE DATA PROVENIENETE DEL ARDUINO###
        data_raw = ardS.readline()
        if data_raw:
            datastr = data_raw.decode("utf-8")
            dsplit = datastr.split(",")
            if (dsplit[0] == 'I'):
                # print(dsplit)
                imu[0] = float(dsplit[1])
                imu[1] = float(dsplit[2])
                imu[2] = float(dsplit[3])
                # imu[3]=imu[2].rstrip('\r\n')
                # imu[4]=float(imu[2])
                continue
            if (dsplit[0] == 'R'):
                rad[0] = dsplit[1]
                rad[1] = float(dsplit[2])
                rad[2] = dsplit[3]
                rad[2] = rad[2].rstrip('\n')
                rad[2] = float(rad[2])
                continue
        else:
            print("no data")
            print('No se pudo enviar la informacion')
            print("Modulos Desactivados")
            ardS.write(b'E')
            ardS.write(b's')
            if (debug):
                conn.close()
            time.sleep(2)
            sys.exit()
        ########LOGICA DE MAZE########
        cmd = mazelogic.logic(rad[0], rad[1], rad[2])
        if (cmd == 'w'):
            adelante(1)
        if (cmd == 'a'):
            izquierda(1)
        if (cmd == 'd'):
            derecha(1)
        if (cmd == 'q'):
            spinizq(1)
        if (cmd == 'e'):
            spinder(1)
        else:
            detenerse()
        ########LOGICA DE MAZE########

        if (debug):
            data = str(rad[1]) + ',' + str(rad[2]) + ',' + str(imu[0]) + ',' + str(imu[1]) + ',' + str(imu[2]) + ',' + 's'
            try:
                conn.sendall(data)
            except socket.error:
                print('No se pudo enviar la informacion')
                print("Modulos Desactivados")
                ardS.write(b'E')
                ardS.write(b's')
                if (debug):
                    conn.close()

                time.sleep(2)
                sys.exit()

        ###ANALISIS DE DATA PROVENIENETE DEL ARDUINO###

        b1S=GPIO.input(b1)
        if (b1S == 1):
            print ("Modulos Desactivados")
            if (debug):
                conn.close()
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()
 #########################MODO MANUAL###############################################
    while b2F == 2: #Modo manual activo
        if ena2S = 1:
            ena2S=0
            for i in range(5): #parpadeo 5 veces modo manual
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(1)  # parpadeo indica modo manual
                GPIO.output(ledS, GPIO.LOW)

        ####conexion TCP ######
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        print('Connected by', addr)
        ####conexion TCP ######
        mov()


        b1S=GPIO.input(b1)
        if (b1S == 1):
            print ("Modulos Desactivados")
            if (debug):
                conn.close()
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()
      

except KeyboardInterrupt :
    print ("Modulos Desactivados")
    if (debug):
        conn.close()
    ardS.write(b"E") 
    ardS.write(b"s") 
    time.sleep(2)
    GPIO.cleanup()
    sys.exit()


