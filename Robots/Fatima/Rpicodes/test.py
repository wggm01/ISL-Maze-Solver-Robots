import time
import csv
import serial
import socket
import sys


ardS = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
imu=[0,0,0,0,0,0,0,0,0,0] # yaw, pitch, roll

HOST= '192.168.25.113'
PORT= 65436
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

def txData (ang,d,yaw,pitch,roll):
    data = str(ang)+','+str(d)+','+str(yaw)+','+str(pitch)+','+str(roll)+','+'s'
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
    
########################################################    

for i in range(0,1):
    ardS.write(b'R') #Activacion de los sensores
    time.sleep(1)
    ardS.write(b's') #fin de mensaje
    time.sleep(0.5)
    print(i)
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
                imu[2]=dsplit[3]
                imu[2]=imu[2].rstrip('\r\n')
                imu[2]=float(imu[2])
                
                continue
            if (dsplit[0]=='R'):
                dire = dsplit[1]
                ang=float(dsplit[2])
                d=dsplit[3]
                d = d.rstrip('\n')
                d = float(d)
                yaw=imu[0]
                pitch=imu[1]
                roll=imu[2]
                txData(ang,d,yaw,pitch,roll)
                #print(dsplit)
                continue
        else:
            
            print ("no data")
        
        
except KeyboardInterrupt:
    print ("Modulos Desactivados")
    ardS.write(b'E') 
    ardS.write(b's')
    conn.close()
    time.sleep(2)
    sys.exit()
