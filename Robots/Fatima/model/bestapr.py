import openpyxl
from openpyxl import load_workbook
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
#array encargado de almacenar data
deg=[0]*41
d=[0]*41
i=0
#cargar documento
wb= load_workbook('reg0-45.xlsx')
sheet= wb['reg0-45']
#iteracion en las celdas
for data in range(1,42): #En lugar de 41 iria el tamano del vector que almacena r
    theta= sheet.cell(row=data, column=1).value
    r= sheet.cell(row=data, column=2).value
    if(r==80 or r<5):
        r=15
    data=data-1
    deg[data]=int(theta)
    d[data]=int(r)
    print(deg[data],d[data])

#Calculo de regresion
slope, intercept, r_value, p_value, std_err = stats.linregress(deg,d)
print("pendiente:",slope,"corte en y",intercept,"r^2",(r_value**2)*100)
theta_test=np.linspace(5,45)
y = slope*theta_test+intercept
#plt.plot(y, theta_test, '-r')
plt.plot(deg, d)
plt.title('Regesion Lineal')
plt.xlabel('Grados', color='#1C2833')
plt.ylabel('Distancia', color='#1C2833')
plt.grid()
plt.show()
