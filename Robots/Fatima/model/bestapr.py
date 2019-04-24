import openpyxl
from openpyxl import load_workbook
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import math
#array encargado de almacenar data
deg=[0]*263
d=[0]*263
x=[0]*263
y=[0]*263
i=0
#cargar documento
wb= load_workbook('test3/reg0-180.xlsx')
sheet= wb['reg0-45']
#iteracion en las celdas
for data in range(1,176): #En lugar de 41 iria el tamano del vector que almacena r
    theta= sheet.cell(row=data, column=1).value
    r= sheet.cell(row=data, column=2).value
    #if (r !=80):
    data=data-1
    deg[data]=math.radians(int(theta))
    x[data]=r*math.cos(math.radians(theta))
        
    d[data]=int(r)
    y[data]=r*math.sin(math.radians(theta))
    #print(deg[data],d[data])

#Calculo de regresion
<<<<<<< HEAD
slope, intercept, r_value, p_value, std_err = stats.linregress(deg,d)
print("pendiente:",slope,"corte en y",intercept,"r^2",(r_value**2)*100)
theta_test=np.linspace(5,45)
y = slope*theta_test+intercept
#plt.plot(y, theta_test, '-r')
plt.plot(deg, d)
=======
#slope, intercept, r_value, p_value, std_err = stats.linregress(deg,d)
#print("pendiente:",slope,"corte en y",intercept,"r^2",(r_value**2)*100)
#theta_test=np.linspace(5,45)
#y = slope*theta_test+intercept
#plt.plot(y, theta_test, '-r')
#plt.polar(deg, d, 'ro')
plt.scatter(x, y)
>>>>>>> 6e6742d98a8b919679303e9984fffdc303dfa935
plt.title('Regesion Lineal')
plt.xlabel('no se como se define', color='#1C2833')
plt.ylabel('Distancia', color='#1C2833')
plt.grid()
plt.show()
