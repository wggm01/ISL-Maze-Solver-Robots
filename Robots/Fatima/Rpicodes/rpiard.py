
import mazelogic # se encarga de la logica en el modo maze(opcion de debugger usando procesing)
import RPi.GPIO as GPIO
import sys
import serial
import time
import os
import socket
GPIO.setmode (GPIO.BCM) #nomenclatura GPIO# no numero de pin
ledS=19 #led  de estado de espera/eleccion de modo
b1=25 #boton para confirmacion de conexion con arduino/MODO MANUAL(activacion en lectura de 1)
b2=16 #boton para modo Maze(activacion en lectura de 1)
nmos=12 #activa rele para encender arduino
GPIO.setwarnings(False)
GPIO.setup(ledS,GPIO.OUT) 
GPIO.setup(nmos,GPIO.OUT) 
GPIO.setup(b1,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #la raspberry actuara cuando reciba 3.3v
GPIO.setup(b2,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
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
debug =0 #control de modo debug
ena_Sensor=0
rst_Sensor=[0]
###CONTROL DE INCIIALIZACION###

###tcp###
imu=[0,0,0] # yaw, pitch, roll
rad=['s',0,0] #'dire','ang','distance'
HOST= '192.168.25.113'
PORT= 6790 # Revisar contra el cliente
###tcp###

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
def txData ():
    data = str(rad[1])+','+str(rad[2])+','+str(imu[0])+','+str(imu[1])+','+str(imu[2])+','+'s'
    try:
        conn.sendall(data)
        
        
    except socket.error:
        print ('No se pudo enviar la informacion')
        print ("Modulos Desactivados")
        ardS.write(b'E') 
        ardS.write(b's')
        conn.close()
        
        time.sleep(2)
        sys.exit()


print("###incio del programa###")
GPIO.output(nmos,GPIO.LOW) #apaga rele
time.sleep(2)
GPIO.output(nmos,GPIO.HIGH) #enciende rele
#ardS = serial.Serial("/dev/serial0", baudrate = 115200) # en espera de level shifter
ardS = serial.Serial("/dev/ttyUSB0", baudrate =9600)

try:
    #Prende Led de estado y espera lectura de boton.
    GPIO.output(ledS,GPIO.HIGH) #enciende led de estado
    
    time.sleep(0.5)#dejar que actue la raspberry
    while (flag == 0):
        print ("Incializando Arduino")
        #b1S=GPIO.input(b1)
        #time.sleep(0.5)
        ardR=ardS.readline()
        ardR1 = ardR.rstrip('\r\n')
        #print(type(ardR1))
        if (ardR1 == '1'): #se sale si presionas b1
            flag=1
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
        
        # control de modo debug:
        while (flag == 1): #bandera flag reutilizada
            print(" Modo Maze-->desea activar modo maze con debug o !debug")
            b1S = GPIO.input(b1)  # lectura de estado de botones
            b2S = GPIO.input(b2)
            time.sleep(0.5)
            if (b1S == 1):  # debug
                flag = 0
                debug=1
            ######TCP INICIALIZACION#####
                
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                except socket.error:
                    print('Error Socket')
                    print("Modulos Desactivados")
                    ardS.write(b'E')
                    ardS.write(b's')
                    time.sleep(2)
					#os.excel("restart.sh","")
                    sys.exit()
					
                s.bind((HOST, PORT))
                s.listen(3)  # Maximo tres clientes
                print("Creando Socket")
                conn, addr = s.accept() #se queda esperando un cliente
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
               
        ######ARDUINO ACTIVACION DE SISTEMA#####
        if (ena_Sensor == 0):
            ena_Sensor = 1
            ardS.write(b'R')  # Activacion de los sensores
            time.sleep(0.080)
            ardS.write(b's')  # fin de mensaje
            print("UART establecido")
        
        ######ARDUINO ACTIVACION DE SISTEMA#####

        ###ANALISIS DE DATA PROVENIENETE DEL ARDUINO###
        
        data_raw = ardS.readline()
        #print(data_raw)
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
                if(dsplit[1]=="CCW"):
                    rad[0] = dsplit[1]
                    rad[1] = float(dsplit[2])
                    rad[2] = dsplit[3]
                    rad[2] = rad[2].rstrip('\r\n')
                    rad[2] = float(rad[2])
                    #print(rad[0], rad[1], rad[2])
                    ########LOGICA DE MAZE########
                    cmd_raw = mazelogic.logic(rad[0], rad[1], rad[2])
                    cmd,ena_Sensor1= cmd_raw
                    #######Movimiento de los motores########
                    #print(cmd)
                    if (cmd == 'w'):                         
                        print ("adelante(1)")
                    if (cmd == 'a'):  
                        print("izquierda(1)")        
                    if (cmd == 'd'):        
                        print("derecha(1)")        
                    if (cmd == 'q'):        
                        print("spinizq(1)")       
                    if (cmd == 'e'):        
                        print("spinder(1)")              
                    else:
                        detenerse()
            if (debug):
                print("Enviado")
                txData()
        else:
            print("no data")
            print('No se pudo enviar la informacion')
            print("Modulos Desactivados")
            ardS.write(b'E')
            ardS.write(b's')
            if (debug):
                conn.close()
            time.sleep(2)
			#os.excel("restart.sh","")
            sys.exit()  
        
        b1S=GPIO.input(b1)
        if (b1S == 1): #detencion del programa manualmente
            print ("Modulos Desactivados")
            if (debug):
                conn.close()
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
			#os.excel("restart.sh","")
            sys.exit()
    
        
 #########################MODO MANUAL###############################################
    while b2F == 2: #Modo manual activo
        print("MODO MANUAL")
        if ena2S == 1:
            ena2S=0
            for i in range(5): #parpadeo 5 veces modo manual
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(1)  # parpadeo indica modo manual
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
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
			#os.excel("restart.sh","")
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


