import RPi.GPIO as GPIO
import time
import csv
import sys

################################################
#Configuracion de los motores y sensor de distancia
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
flag=0 #inicio de procesos una sola vez
#################
regC=[0,0,0,0]
pnt0=[0]*47 #0-45
pnt1=[0]*47 #46-90
pnt2=[0]*47 #90-135
pnt3=[0]*47 #136-180
suma=[0,0,0,0]#sumatorias
movlog=[0,0,0,0] #decide el movimiento
noexit=[0]*20000
i=0
#################
regC_cw=[0,0,0,0]
pnt0_cw=[0]*47 #0-45
pnt1_Cw=[0]*47 #46-90
pnt2_cw=[0]*47 #90-135
pnt3_cw=[0]*47 #136-180
suma_cw=[0,0,0,0]#sumatorias
movlog_cw=[0,0,0,0] #decide el movimiento
noexit_cw=[0]*20000
i_cw=0
#################
idle=[0,0]#indicador de proceso completo
rmov=[0,0] #redundancia
#################
################################################
#Movimientos del robot
def adelante(mode):
    ena.ChangeDutyCycle(90) #duty cycle
    enb.ChangeDutyCycle(90)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.HIGH)
    if mode == 1:
            time.sleep(2.5)
            detenerse()

def izquierda(mode):
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.LOW)
    if mode == 1:
            time.sleep(1.5)
            detenerse()
    
def spinizq(mode):
    ena.ChangeDutyCycle(75)
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.HIGH)
    GPIO.output(motorB1,GPIO.HIGH)
    GPIO.output(motorB2,GPIO.LOW)
    if mode == 1:
            time.sleep(1.5)
            detenerse()

def derecha(mode):
    enb.ChangeDutyCycle(75)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB2,GPIO.HIGH)
    if mode == 1:
            time.sleep(1.5)
            detenerse()

def spinder(mode):
    enb.ChangeDutyCycle(75)
    ena.ChangeDutyCycle(75)
    GPIO.output(motorA1,GPIO.HIGH)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB2,GPIO.HIGH)
    if mode == 1:
            time.sleep(1.5)
            detenerse()

def detenerse():
    ena.ChangeDutyCycle(0)
    enb.ChangeDutyCycle(0)
    GPIO.output(motorA1,GPIO.LOW)
    GPIO.output(motorA2,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    GPIO.output(motorB1,GPIO.LOW)
    
########################################
def sendData(dataRaw,sync):
    while sync.get() == 1:
        if dataRaw.empty() is False:
            data = data.Raw.get()
            put('http://192.168.0.243:80/sensor', data={'data':data}).json()
            with open('graphlog.csv','a') as f:
                f.write("%s\n" % ( data))
            
#######################################
            
#######################################
####################################
def awd(gyrox,gyroy,gyroz,accx,accy,accz,magx,magy,magz):
    print ("en construccion")
####################################

def logic(dire,theta,r):
    if 1 == 1:
        if 1==1:
            if dire == "ccw":
                if(theta<46):
                    #cantidad de puntos [para realizar el promedio]
                    pnt0[regC[0]]=r
                    regC[0] +=1 # Realiza el incremento para ir guardando las r en pnt
                    #promedio de distancia[max dist 38cm]
                    if theta== 45:
                        for i in pnt0:
                            suma[0]= suma[0]+ i
                        prom=suma[0]/len(pnt0)
                        if prom <= 38:
                            movlog[0]=1 #instruccion logica para movimiento de robot
                            regC[0]=0 # reincia contador para nuevo analisis
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog[0]=0
                            regC[0]=0 # reincia contador para nuevo analisis
       
                elif(theta>45 and theta<91):
                    #cantidad de puntos [para realizar el promedio]
                    pnt1[regC[1]]=r
                    regC[1] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 90:
                        for i in pnt1:
                            suma[1]= suma[1]+ i
                        prom=suma[1]/len(pnt1)
                        if prom <= 38:
                            movlog[1]=1
                            regC[1]=0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog[1]=0
                            regC[1]=0
                        
                elif(theta>90 and theta<136):
                    #cantidad de puntos [para realizar el promedio]
                    pnt2[regC[2]]=r
                    regC[2] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 135:
                        for i in pnt2:
                            suma[2]= suma[2]+ i
                        prom=suma[2]/len(pnt2)
                        if prom <= 38:
                            movlog[2]=1
                            regC[2]=0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog[2]=0
                            regC[2]=0
                        
                elif(theta>135 and theta<181):
                    #cantidad de puntos [para realizar el promedio]
                    pnt3[regC[3]]=r
                    regC[3] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 180:
                        for i in pnt3:
                            suma[3]= suma[0]+ i
                        prom=suma[3]/len(pnt3)
                        if prom <= 38:
                            movlog[3]=1
                            regC[3] =0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog[3]=0
                            regC[3]=0
                elif theta == 180:
        
                    #decision de movimiento:
                    rmov[0]= str(movlog[0])+str(movlog[1])+str(movlog[2])+str(movlog[3])
                    print (rmov[0])
                    idle[0]=1
                    if mov == "1001":
                        #avanzar recto
                        adelante(1)
                    if mov == "0001":
                        #avanzar izquierda 90 grados
                        spinizq(1)
                    if mov == "1000":
                        #avanzar derecha 90 grados
                        spinder(1)
                    if mov == "1111":
                        #rotar 180
                        spinizq()
                        #almacenar sin salida
                        i +=1
                        noexit[i]= 1
############################################################                        
            elif dire == "cw":
                if(theta>170 and theta <136):
                    #cantidad de puntos [para realizar el promedio]
                    pnt0_cw[regC_cw[0]]=r
                    regC_cw[0] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 135:
                        for i in pnt0_cw:
                            suma_cw[0]= suma_cw[0]+ i
                        prom=suma_cw[0]/len(pnt0_cw)
                        if prom <= 38:
                            movlog_cw[3]=1
                            regC_cw[0]=0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog_cw[3]=0
                            regC_cw[0]=0
       
                elif(theta>134 and theta<91):
                    #cantidad de puntos [para realizar el promedio]
                    pnt1_cw[regC_cw[1]]=r
                    regC_cw[1] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 90:
                        for i in pnt1_cw:
                            suma_cw[1]= suma_cw[1]+ i
                        prom=suma_cw[1]/len(pnt1_cw)
                        if prom <= 38:
                            movlog_cw[2]=1
                            regC_cw[1]=1
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog_cw[2]=0
                            regC_cw[1]=1
                        
                elif(theta>89 and theta<46):
                    #cantidad de puntos [para realizar el promedio]
                    pnt2[regC_cw[2]]=r
                    regC_cw[2] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 45:
                        for i in pnt2_cw:
                            suma_cw[2]= suma_cw[2]+ i
                        prom=suma_cw[2]/len(pnt2_cw)
                        if prom <= 38:
                            movlog_cw[1]=1
                            regC_cw[2]=0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog_cw[1]=0
                            regC_cw[2]=0
                        
                elif(theta<46):
                    #cantidad de puntos [para realizar el promedio]
                    pnt3[regC_cw[3]]=r
                    regC_cw[3] +=1
                    #promedio de distancia[max dist 38cm]
                    if theta== 180:
                        for i in pnt3_cw:
                            suma_cw[3]= suma_cw[0]+ i
                        prom=suma[3]/len(pnt3_cw)
                        if prom <= 38:
                            movlog_cw[0]=1
                            regC_cw[3] =0
                        else:
                            #obstaculo logico[1=pared, 0=libre]
                            movlog_cw[0]=0
                            regC_cw[3]=0
                            
                elif theta == 0:
                    #decision de movimiento:
                    rmov[1]= str(movlog[0])+str(movlog[1])+str(movlog[2])+str(movlog[3])
                    idle[1]=1
                            
            elif idle[0]*idle[1] == 1:
                
                if rmov[0]==rmov[1]:
                    if mov == "1001":
                        #avanzar recto
                        adelante(1)
                    if mov == "0001":
                        #avanzar izquierda 90 grados
                        spinizq(1)
                    if mov == "1000":
                        #avanzar derecha 90 grados
                        spinder(1)
                    if mov == "1111":
                        #rotar 180
                        spinizq()
                        #almacenar sin salida
                        i +=1
                        noexit[i]= 1
            else:
                print ("mapeando")
                    

######################################

