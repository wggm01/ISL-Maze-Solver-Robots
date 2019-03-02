import time
import csv
import serial
import socket
import sys

imu=[0,0,0] # yaw, pitch, roll
rad=['s',0,0] #'dire','ang','distance'
HOST= '192.168.25.113'
PORT= 6790

#######################################################
print("Creando Socket")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
except socket.error:
    print('Error Socket')
    print ("Modulos Desactivados")
    time.sleep(2)
    sys.exit()
    
s.bind((HOST, PORT))

s.listen(3) #Maximo tres clientes

conn, addr = s.accept()

print('Connected by', addr)

    

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
print("Esperando a que termine la calibracion del imu")
ardS = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
time.sleep(20)
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
#            print(dsplit)
            if (dsplit[0] == 'I'):
#                print(dsplit)
                imu[0]=float(dsplit[1])
                imu[1]=float(dsplit[2])
                imu[2]=float(dsplit[3])
#                print(imu[0],imu[1],imu[2]) 
                continue
            if (dsplit[0]=='R'):
#                print(dsplit)
                rad[0] = dsplit[1]
                rad[1]=float(dsplit[2])
                rad[2]=dsplit[3]
                rad[2] = rad[2].rstrip('\r\n')
                rad[2] = float(rad[2])
#                print(rad[0],rad[1],rad[2]) 
                continue
        else:
            print ("no data")
        txData()
except KeyboardInterrupt:
    print ("Modulos Desactivados")
    ardS.write(b'E') 
    ardS.write(b's')
    conn.close()
    time.sleep(2)
    sys.exit()
