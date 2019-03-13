import time
import csv
import serial
import socket
import sys
from _thread import*

ardS = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
imu=[0,0,0] # yaw, pitch, roll
rad=['s',0,0] #'dire','ang','distance'
HOST= '192.168.25.113'
PORT= 65437
#######################################################
print("Creando Socket")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Error Socket')
    print ("Modulos Desactivados")
    ardS.write(b'E') 
    ardS.write(b's')
    time.sleep(2)
    sys.exit()
    
s.bind((HOST, PORT))
s.listen(3) #Maximo tres clientes
conn, addr = s.accept()
print('Connected by', addr)

#Creacion de thread
def client_thread(conn,rad,imu):
    
    try:
        data = str(rad[1])+','+str(rad[2])+','+str(imu[0])+','+str(imu[1])+','+str(imu[2])+','+'s'
        conn.sendall(data)
        print("Termine_Thread")
    except socket.error:
        print ('No se pudo enviar la informacion')
        print ("Modulos Desactivados")
        ardS.write(b'E') 
        ardS.write(b's')
        conn.close()
        time.sleep(2)
        sys.exit()
    
########SIN USO POR EL MOMENTO###########
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
    
##########SIN USO POR EL MOMENTO###########    

##########ADQUISICION DE CLIENTES##########
for i in range(3):
    conn, addr = s.accept()
    print('Connected by', addr)
##########ADQUISICION DE CLIENTES##########

for i in range(0,1):
    ardS.write(b'R') #Activacion de los sensores
    time.sleep(1)
    ardS.write(b's') #fin de mensaje
    time.sleep(0.5)
    print("Intentando conectar")
print("UART establecido")
 
try:
    while (True):
        data_raw = ardS.readline()
        if data_raw:    
            datastr= data_raw.decode("utf-8")
            dsplit=datastr.split(",")
            if (dsplit[0] == 'I'):
                #print(dsplit)
                imu[0]=float(dsplit[1])
                imu[1]=float(dsplit[2])
                imu[2]=float(dsplit[3])
                #imu[3]=imu[2].rstrip('\r\n')
                #imu[4]=float(imu[2])      
                continue
            if (dsplit[0]=='R'):
                rad[0] = dsplit[1]
                rad[1]=float(dsplit[2])
                rad[2]=dsplit[3]
                rad[2] = rad[2].rstrip('\n')
                rad[2] = float(rad[2])
                continue
        else:
            print ("no data")
        
        start_new_thread(client_thread, (conn,rad,imu,))
except KeyboardInterrupt:
    print ("Modulos Desactivados")
    ardS.write(b'E') 
    ardS.write(b's')
    conn.close()
    time.sleep(2)
    sys.exit()
