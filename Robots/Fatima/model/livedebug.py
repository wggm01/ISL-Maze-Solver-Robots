import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import collections
import math
import socket
from time import sleep as delay

#Conexion por TCP
server_address = ('192.168.0.247',6793)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

interval = int(0.0001*1000) #coloca al intervalo en ms
bufsize = int(0.0351/0.0001)#recibire maximo 351 puntos del radar
databufferx = collections.deque([0.0]*bufsize, bufsize)
databuffery = collections.deque([0.0]*bufsize, bufsize)
x = np.linspace(-30., 30.,bufsize) #esto se mantiene
y = np.zeros(bufsize, dtype=np.float)
fig = plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.set_title('reg0-180')
ax1.set_xlim([-30,30])
ax1.set_ylim([0,30])
ax1.set_xlabel('Distancia horizontal con respecto al sensor')
ax1.set_ylabel('Distancia vertical')
ax1.scatter(x,y,color='black')


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
    databufferx.append(rectx)
    databuffery.append(recty)
    x[:] = databufferx
    y[:] = databuffery
    
    ax1.set_offsets(x,y)
       
    if(deg==180):
        ax1.clear()

ani = animation.FuncAnimation(fig,animate,interval=0.1) #Intervalo de ejecucion de funcion animate en ms
plt.show()
