import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import socket
from time import sleep as delay

#Conexion por TCP
server_address = ('192.168.0.247',6792)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

fig = plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.set_title('reg0-180')
ax1.set_xlim([-30,30])
ax1.set_ylim([0,30])
ax1.set_xlabel('Distancia horizontal con respecto al sensor')
ax1.set_ylabel('Distancia vertical')


def animate(i):
    data = s.recv(8)
    data_decode=data.decode("utf-8")
    data_str=str(data_decode)
    packet_slice=data_str.partition('s')
    deg,distance=packet_slice[0].split(",")
    deg=float(deg)
    distance=float(distance)
    rectx=distance*math.cos(math.radians(deg))
    recty=distance*math.sin(math.radians(deg))
    ax1.scatter(rectx,recty,color='black')
#    if data < 0:
#        print("Modulos Desactivados")
#        s.close()
#        ax1.close()
        
    #clustering basikito
    if(deg<45):
        rectx=distance*math.cos(math.radians(deg))
        recty=distance*math.sin(math.radians(deg))
        ax1.scatter(rectx,recty,color='black')
      
    if(deg > 45 and deg < 91):
        rectx=distance*math.cos(math.radians(deg))
        recty=distance*math.sin(math.radians(deg))
        ax1.scatter(rectx,recty,color='yellow')
       

    if(deg > 90 and deg < 136):
        rectx=distance*math.cos(math.radians(deg))
        recty=distance*math.sin(math.radians(deg))
        ax1.scatter(rectx,recty,color='cyan')
     

    if(deg > 135 and deg < 181):
        rectx=distance*math.cos(math.radians(deg))
        recty=distance*math.sin(math.radians(deg))
        ax1.scatter(rectx,recty,color='purple')
       
    if(deg==180):
        ax1.clear()

ani = animation.FuncAnimation(fig,animate,interval=0.1) #Intervalo de ejecucion de funcion animate en ms
plt.show()
