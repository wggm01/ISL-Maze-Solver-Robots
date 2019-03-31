# instalar pip install mpu9250 https://github.com/MomsFriendlyRobotCompany/mpu9250
# pip install FaBo9Axis_MPU9250 https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python
import math
import RPi.GPIO as GPIO
import sys
import time
import os
import socket
GPIO.setmode (GPIO.BCM) #nomenclatura GPIO# no numero de pin
ledS=19 #led  de estado de espera/eleccion de modo
b1=25 #boton para confirmacion de conexion con arduino/MODO MANUAL(activacion en lectura de 1)
b2=16 #boton para modo Maze(activacion en lectura de 1)
TRIG = 23#ver cual esta libre
ECHO = 24#ver cual esta libre
SERVO= 25 #ver cual esta libre
timeout=[0]
####imu variables###
RAD_TO_DEG = 57.295779513082320876798154814105 #valor para realizar conversiones de radianes a grados
#variables para realizar el calculo de angulos de euler
grxyz=[0,0,0]#gyroRatex,gyroRatey,gyroRatez;
gpry = [0,0,0] #gpitch,groll,gyaw;
arxyz=[0,0,0]#accRatex,accRatey,accRatez;
accpr=[0,0]#accpitch,accroll;
pry=[0,0,0]#pitch,roll,yaw;#variables para realizar el calculo de angulos de euler
####imu variables###
#VARIBALES DE LOGICA DE MAZE##
#######CCW##########
regC=[0,0,0,0] #Incrementador para ir guardando distancias
pnt0=[0]*100 #5-45
pnt1=[0]*100 #46-90
pnt2=[0]*100 #90-135
pnt3=[0]*100 #136-180
average=[0,0,0,0]#sumatorias
movlog=[0,0,0,0] #decide el movimiento

#######CW##########
regC_cw=[0,0,0,0] #Incrementador para ir guardando distancias
pnt0_cw=[0]*100 #5-45
pnt1_Cw=[0]*100 #46-90
pnt2_cw=[0]*100 #90-135
pnt3_cw=[0]*100 #136-180
average_cw=[0,0,0,0]#sumatorias
movlog_cw=[0,0,0,0] #decide el movimiento
#################
idle=[0,0]#indicador de proceso completo
rmov=[0,0] #redundancia
#################
#VARIABLES DE LOGICA DE MAZE##
GPIO.setwarnings(False)
####Control####
GPIO.setup(ledS,GPIO.OUT)
GPIO.setup(b1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #la raspberry actuara cuando reciba 3.3v
GPIO.setup(b2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
####Control####
###Servo###
GPIO.setup(SERVO,GPIO.OUT)
SRV=GPIO.PWM(SERVO,500)
SRV.start(0)
###Servo###
####HC-SR04###
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
####HC-SR04###

####INCIALIZACION DE PINES PARA L298N####
motorA1=4 # in1
motorA2=23# in3
motorB1=17# in2
motorB2=22# in4
motorena=18
motorenb=26
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
flag1=0 #se encarga de salir del while en el que se elije el modo debug
b1F=0 #elige el modo maze
b2F=0 #elige el modo manual
enaS=1 # Flag para correr codigo una sola vez
ena2S=1 #Flag para correr codigo una sola vez
debug =[0] #control de modo debug
###CONTROL DE INCIIALIZACION###

###tcp###
imu=[0,0,0] # yaw, pitch, roll
rad=['s',0,0] #'dire','ang','distance'
HOST= '192.168.25.113'
PORT= 6790 # Revisar contra el cliente
###tcp###

############Data de sensores####################
def imu():
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
            timeout[0]=0
            break
        else:
            timeout[0]=1
            break

    if (timeout[0]==1):
        while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

        pulse_duration = (pulse_end - pulse_start)*1000000

    distance = int(0.01715 * pulse_duration)
    return distance
def dutyCycle(theta):
    dc=1 #ecuacion
    SRV.ChangeDutyCycle(dc)
############Data de sensores####################
#####Envio de data#####
def txData(rad[1],rad[2],imu[0],imu[1],imu[2],debug[0]):
    ########ENVIO DE DATOS########
    if (debug[0]):
        data = str(rad[1]) + ',' + str(rad[2]) + ',' + str(imu[0]) + ',' + str(imu[1]) + ',' + str(imu[2]) + ',' + 's'
        try:
            conn.sendall(data)
        except socket.error:
            print('No se pudo enviar la informacion')
            print("Modulos Desactivados")

            if (debug):
                conn.close()
            time.sleep(2)
            # os.excel("restart.sh","")
            sys.exit()
    ########ENVIO DE DATOS########
#####Envio de data#####
######Movimiento de los motores######
def detenerse():
    ena.ChangeDutyCycle(0)
    enb.ChangeDutyCycle(0)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
	
	
def adelante(mode):
    ena.ChangeDutyCycle(80)  # duty cycle
    enb.ChangeDutyCycle(80)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1) # ajustar hasta implementar encoder
        detenerse()


def izquierda(mode):
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    if mode == 1:
        time.sleep(1) # ajustar hasta implementar encoder
        detenerse()


def spinizq(mode):
    ena.ChangeDutyCycle(75)
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.HIGH)
    GPIO.output(motorB1, GPIO.HIGH)
    GPIO.output(motorB2, GPIO.LOW)
    if mode == 1:
        time.sleep(1) # ajustar hasta implementar encoder
        detenerse()


def derecha(mode):
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1) # ajustar hasta implementar encoder
        detenerse()


def spinder(mode):
    enb.ChangeDutyCycle(75)
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1, GPIO.HIGH)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.HIGH)
    if mode == 1:
        time.sleep(1) # ajustar hasta implementar encoder
        detenerse()

######Movimiento de los motores######

#####LOGICA DE MAZE[UN SOLO SENTIDO DE BARRIDO]#####
def logic(dire, theta, r):
    # print (dire,theta,r)
    # dire=str(dire)
    if dire == "CCW":

        if (theta < 46):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt0[regC[0]] = r
            regC[0] += 1  # Realiza el incremento para ir guardando las r en pnt
            # promedio de distancia[max dist 38cm]
            if theta == 45:
                average[0] = sum(pnt0) / len(pnt0)
                # print("0-45 ",average[0])
                if (average[0]) < 40:
                    movlog[0] = 1  # instruccion logica para movimiento de robot
                    regC[0] = 0  # reincia contador para nuevo analisis
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[0] = 0
                    regC[0] = 0  # reincia contador para nuevo analisis


        elif (theta > 45 and theta < 91):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt1[regC[1]] = r
            regC[1] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 90:
                average[1] = sum(pnt1) / len(pnt1)
                # print("45-90 ",average[1])
                if (average[1]) < 40:
                    movlog[1] = 1  # instruccion logica para movimiento de robot
                    regC[1] = 0  # reincia contador para nuevo analisis
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[1] = 0
                    regC[1] = 0


        elif (theta > 90 and theta < 136):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt2[regC[2]] = r
            regC[2] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 135:
                average[2] = sum(pnt2) / len(pnt2)
                # print("90-136 ",average[2])
                if (average[2]) < 40:
                    movlog[2] = 1
                    regC[2] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[2] = 0
                    regC[2] = 0

        elif (theta > 135 and theta < 181):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt3[regC[3]] = r
            regC[3] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 180:
                average[3] = sum(pnt3) / len(pnt3)
                # print("136-180 ",average[3])
                if (average[3]) < 40:
                    movlog[3] = 1
                    regC[3] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[3] = 0
                    regC[3] = 0

        if theta == 180:
            # decision de movimiento:
            rmov[0] = str(movlog[0]) + str(movlog[1]) + str(movlog[2]) + str(movlog[3])
            # print(rmov[0])
            idle[0] = 1  # identificador de que se completo el analisis en ccw

            if idle[0] == 1:
                if rmov[0] == "1001":
                    # avanzar recto
                    idle[0] = 0
                    # idle[1] = 0
                    adelante(1)

                if rmov[0] == "0001":
                    # avanzar izquierda 90 grados
                    idle[0] = 0
                    # idle[1] = 0
                    izquierda(1)

                if rmov[0] == "1000":
                    # avanzar derecha 90 grados
                    idle[0] = 0
                    # idle[1] = 0
                    derecha(1)

                if rmov[0] == "1111":
                    # rotar 180
                    idle[0] = 0
                    # idle[1] = 0
                    spinizq(1)

                else:
                    return ('x', 1)
                    print("mapeando")


#####LOGICA DE MAZE####

print("###incio del programa###")

try:
    #Prende Led de estado y espera lectura de boton.
    GPIO.output(ledS,GPIO.HIGH) #enciende led de estado
    
    time.sleep(0.5)#dejar que actue la raspberry

    GPIO.output(ledS,GPIO.LOW)

    time.sleep(0.5) #esperar por cualquier eventualidad
    b1S=GPIO.input(b1) #ALMACENO EL ESTADO inicial
    b2S=GPIO.input(b2) #ALMACENO EL ESTADO inicial

    if (b1S==1 and b2S == 1): #SIN  PRESIONAR ESTA EN ALTO
        print("No puede presionar ambos botones a la vez")
    else:
        while (b1S==0 and b2S == 0): #permanecera en el loop hasta que se presione un boton
            print("elija el modo")
            b1S=GPIO.input(b1) #ALMACENO EL ESTADO ACTUAL
            time.sleep(0.5)
            if (b1S == 1):
                b1F=1 #bandera para modo maze
                #print(b1F)
                break
            b2S=GPIO.input(b2) #ALMACENO EL ESTADO ACTUAL
            time.sleep(0.5)
            if (b2S==1):
                b2F=2 #bandera para modo manual
                #print(b2F)
                break #SALE DEL WHILE SI ALGUNO DE LOS DOS ES PRESIONADO
####################MODO MAZE###################################
    while b1F == 1: #Modo maze activo

        if flag1 == 0:  #bandera flag1
            flag1 = 1
            for i in range(10):  # parpadeo de led 10 veces para elegir debug o !debug
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(ledS, GPIO.LOW)

        # control de modo debug:
        while (flag == 0): #bandera flag
            print(" Modo Maze-->desea activar modo maze con debug o !debug")
            b1S = GPIO.input(b1)  # lectura de estado de botones
            b2S = GPIO.input(b2)
            time.sleep(0.5)
            if (b1S == 1):  # debug
                flag = 1
                debug[0]=1
            ######TCP INICIALIZACION#####
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error:
                    print('Error Socket')
                    print("Modulos Desactivados")
                    time.sleep(2)
					#os.excel("restart.sh","")
                    sys.exit()
					
                s.bind((HOST, PORT))
                s.listen(3)  # Maximo tres clientes
                print("Creando Socket")
                #reverificacion de orden de debug
                while (check== 0):
                    GPIO.output(ledS, GPIO.HIGH)
                    time.sleep(0.5)
                    GPIO.output(ledS, GPIO.LOW)
                    print("Esta seguro debug o !debug?")
                    b2S = GPIO.input(b2)
                    b1S = GPIO.input(b1)
                    time.sleep(0.5)
                    if (b2S == 1):  # debug
                        check = 1
                        debug[0] = 0
                    if (b1S == 1):
                # reverificacion de orden de debug
                    conn, addr = s.accept() #se queda esperando un cliente
                    print('Connected by', addr)
                    break
            ######TCP INICIALIZACION#####
                break
            if (b2S == 1):  # !debug
                flag = 1
                debug[0] =0
                break

        if enaS == 1:  # una sola ejecucion
            enaS = 0
            for i in range(3):  # parpadeo de led de estado 3 veces indica modo maze.
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(ledS, GPIO.LOW)
               
        ######Servo, IMU ADQUISIOCION DE DATOS#####
        for ccw in range(1,180):
            dutyCycle(ccw)
            time.sleep(0.5)
            rad[0] = "CCW"
            rad[1] = ccw
            rad[2] = hcsr04()
            imu[0], imu[1], imu[2] = imu()
            logic(rad[0],rad[1], rad[2])
            txData(rad[1],rad[2],imu[0],imu[1],imu[2],debug[0])
            b1S = GPIO.input(b1)
            if (b1S == 1):  # detencion del programa manualmente
                print("Modulos Desactivados")
                if (debug):
                    conn.close()
                time.sleep(2)
                GPIO.cleanup()
                # os.excel("restart.sh","")
                sys.exit()
        for cw in range(180, 1, -1):
            dutyCycle(cw)
            time.sleep(0.5)
#            rad[0] = "CW"
#            rad[1]= cw
#            rad[2] = hcsr04()
#            imu[0],imu[1],imu[2]= imu()
#            logic(rad[0], rad[1], rad[2])
#            txData(rad[1], rad[2], imu[0], imu[1], imu[2], debug[0])
#            b1S = GPIO.input(b1)
            if (b1S == 1):  # detencion del programa manualmente
                print("Modulos Desactivados")
                if (debug):
                    conn.close()
                time.sleep(2)
                GPIO.cleanup()
                # os.excel("restart.sh","")
                sys.exit()
        ######Servo, IMU ADQUISIOCION DE DATOS#####

 #########################MODO MANUAL###############################################
    while b2F == 2: #Modo manual activo
        print("MODO MANUAL")
        if ena2S == 1:
            ena2S=0
            for i in range(5): #parpadeo 5 veces modo manual
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(0.5)  # parpadeo indica modo manual
                GPIO.output(ledS, GPIO.LOW)

            ####conexion TCP ######
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((HOST, PORT))
            s.listen(5)
            print("Creando Socket")
            conn, addr = s.accept()
            print('Connected by', addr) #se queda esperando un cliente
            ####conexion TCP ######
            
        ###control manual###
        data = conn.recv(1024)
        if not data:
            print("Modulos Desactivados")
            conn.close()
            time.sleep(2)
            GPIO.cleanup()
            #os.excel("restart.sh","")
            sys.exit()

        # ANALISIS DE DATA
        cmdRaw = data.partition('s') # Separa la trama al encontrar el caracter s (cmd,s,'')
        cmd= cmdRaw[0] # (cmd)
        #comando = realizar un movimiento
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
            #os.excel("restart.sh","")
            sys.exit()
            
        if (cmd == 'z'):
            detenerse() #se enviara una z indicando que el boton ha sido soltado.
        ###control manual###
        
        print("Modo manual Activo")

        b1S=GPIO.input(b1)
        if (b1S == 1): #detencion del programa manualmente
            print ("Modulos Desactivados")
            conn.close()
            time.sleep(2)
            GPIO.cleanup()
			#os.excel("restart.sh","")
            sys.exit()
      

except KeyboardInterrupt :
    print ("Modulos Desactivados")
    if (debug):
        conn.close()
    time.sleep(2)
    GPIO.cleanup()
    sys.exit()


