import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import socket

#Conexion por TCP
server_address = ('192.168.25.117',6790)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)

fig = plt.figure()
ax1=fig.add_subplot(1,1,1)
ax1.set_title('reg0-180')
ax1.set_xlim([-30,30])
ax1.set_ylim([0,30])

def animate(i):
    data = s.recv(1024)
    data=data.decode("utf-8")
    frame = data.partition('s')
    fradar=frame[0]
    print(fradar)
    #grado,distania,pitch,roll,yaw,s (formato de data)
#    if not data:
#        print("Modulos Desactivados")
#        s.close()
#        ax1.close()
#    deg = frame[0]
#    distance = frame[1]
    #clustering basikito
#    if(deg<45):
#        rectx=distance*math.cos(math.radians(deg))
#        recty=distance*math.sin(math.radians(deg))
#        ax1.set_xlim([-30,30])
#        ax1.set_ylim([0,30])
#        ax1.plot(rectx,recty,color='green', marker='ro')
#        ax1.set_xlabel('Distancia horizontal con respecto al sensor')
#        ax1.set_ylabel('Distancia vertical')


#    if(deg > 45 and deg < 91):
#        rectx=distance*math.cos(math.radians(deg))
#        recty=distance*math.sin(math.radians(deg))
#        ax1.set_xlim([-30,30])
#        ax1.set_ylim([0,30])
#        ax1.plot(rectx,recty,color='green', marker='ro')
#        ax1.set_xlabel('Distancia horizontal con respecto al sensor')
#        ax1.set_ylabel('Distancia vertical')


#    if(deg > 90 and deg < 136):
#        rectx=distance*math.cos(math.radians(deg))
#        recty=distance*math.sin(math.radians(deg))
#        ax1.set_xlim([-30,30])
#        ax1.set_ylim([0,30])
#        ax1.plot(rectx,recty,color='green', marker='ro')
#        ax1.set_title('reg0-45')
#        ax1.set_xlabel('Distancia horizontal con respecto al sensor')
#        ax1.set_ylabel('Distancia vertical')


#    if(deg > 135 and deg < 181):
#        rectx=distance*math.cos(math.radians(deg))
#        recty=distance*math.sin(math.radians(deg))
#        ax1.clear()
#        ax1.set_xlim([-30,30])
#        ax1.set_ylim([0,30])
#        ax1.plot(rectx,recty,color='green', marker='ro')
#        ax1.set_title('reg0-45')
#        ax1.set_xlabel('Distancia horizontal con respecto al sensor')
#        ax1.set_ylabel('Distancia vertical')
#        if(deg==180):
#            ax1.clear()

ani = animation.FuncAnimation(fig,animate,interval=5) #Intervalo de ejecucion de funcion animate en ms
plt.show()
