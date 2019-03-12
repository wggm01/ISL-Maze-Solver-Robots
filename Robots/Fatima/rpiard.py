
from mazedist import logic # se encarga de la logica en el modo maze(opcion de debugger usando procesing)
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
flag=0 #activa la secuencia de activacion y acepta el modo debug
flag1=0 #me ayuda a negar el modo debug solamente
b1F=0 #elige el modo maze
b2F=0 #elige el modo manual
enaS=1 #asegura que se envie la data por uart solo una vez
debug =0 #control de modo debug
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

    while b1F == 1: #Modo maze activo
        print("MODO MAZE")
        if enaS == 1:
            ardS.close() #una sola ejecucion
            enaS=0
            GPIO.output(ledS, GPIO.HIGH)
            time.sleep(0.05)  # parpadeo indica modo maze
            GPIO.output(ledS, GPIO.LOW)
            #control de modo debug:
            while (flag == 1):
                GPIO.output(ledS, GPIO.HIGH)
                time.sleep(0.5) #parpadeo indica si quiero activar el modo debug
                GPIO.output(ledS, GPIO.LOW)
                print("desea activar modo debug")
                b1S = GPIO.input(b1) #lectura de estado de botones
                b2S = GPIO.input(b2)
                time.sleep(0.5)
                if (b1S == 1):  # se sale si presionas b1 activando el modo debug
                    flag = 0
                    debug=1
                    break
                if (b2S == 1):  # se sale si presionas b1
                    flag = 0
                    debug=0
                    break
        status=logic(debug) #debug indicara si se activa el servidor tcp
            if (!status):
                print("Modulos Desactivados")
                ardS.open()
                ardS.write(b"E")  # Desactiva los sensores
                ardS.write(b"s")
                time.sleep(2)
                GPIO.cleanup()
                sys.exit()

        b1S=GPIO.input(b1)
        if (b1S == 1):
            print ("Modulos Desactivados")
            ardS.open()
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()
            
    while b2F == 2: #Modo manual activo
        GPIO.output(ledS, GPIO.HIGH)
        time.sleep(0.25)  # parpadeo indica modo manual
        GPIO.output(ledS, GPIO.LOW)
        status = mov()
        if (!status):
            print("Modulos Desactivados")
            ardS.open()
            ardS.write(b"E")  # Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()

        b1S=GPIO.input(b1)
        if (b1S == 1):
            ardS.open()
            print ("Modulos Desactivados")
            ardS.write(b"E") #Desactiva los sensores
            ardS.write(b"s")
            time.sleep(2)
            GPIO.cleanup()
            sys.exit()
      

except KeyboardInterrupt :
    print ("Modulos Desactivados")
    ardS.open()
    ardS.write(b"E") 
    ardS.write(b"s") 
    time.sleep(2)
    GPIO.cleanup()
    sys.exit()


