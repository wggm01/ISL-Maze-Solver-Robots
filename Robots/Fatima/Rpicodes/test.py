import time
import sys
import bluetooth

HOST= ''
PORT= 1

server=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print("SOCKET")
try:
    server.bind((HOST,PORT))
    print("BINDED")
except:
    print("D:")
server.listen(1)
print("Esperando a cliente")
client, address=server.accept()

print(address,client)

try:
    while (True):
        data=client.recv(1024)
        print(data)
        
except KeyboardInterrupt:
    print ("Modulos Desactivados")
    client.close()
    server.close()
    time.sleep(2)
    sys.exit()
