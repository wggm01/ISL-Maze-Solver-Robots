
import time
#######CCW##########
regC=[0,0,0,0] #Incrementador para ir guardando distancias
pnt0=[0]*47 #5-45
pnt1=[0]*47 #46-90
pnt2=[0]*47 #90-135
pnt3=[0]*47 #136-180
average=[0,0,0,0]#sumatorias
movlog=[0,0,0,0] #decide el movimiento

#######CW##########
regC_cw=[0,0,0,0] #Incrementador para ir guardando distancias
pnt0_cw=[0]*47 #5-45
pnt1_Cw=[0]*47 #46-90
pnt2_cw=[0]*47 #90-135
pnt3_cw=[0]*47 #136-180
average_cw=[0,0,0,0]#sumatorias
movlog_cw=[0,0,0,0] #decide el movimiento
#################
idle=[0,0]#indicador de proceso completo
rmov=[0,0] #redundancia
#################

def logic(dire,theta,r):
    if dire == "ccw":
        if (theta < 46): #check
            # cantidad de puntos [para realizar el promedio]
            pnt0[regC[0]] = r
            regC[0] += 1  # Realiza el incremento para ir guardando las r en pnt
            # promedio de distancia[max dist 38cm]
            if theta == 45:
                average[0] = sum(pnt0) / len(pnt0)
                if average[0] < 40:
                    movlog[0] = 1  # instruccion logica para movimiento de robot
                    regC[0] = 0  # reincia contador para nuevo analisis
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[0] = 0
                    regC[0] = 0  # reincia contador para nuevo analisis


        elif (theta > 45 and theta < 91):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt1[regC[1]] = r
            regC[1] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 90:
                average[1] = sum(pnt1) / len(pnt1)
                if average[1] < 40:
                    movlog[1] = 1  # instruccion logica para movimiento de robot
                    regC[1] = 0  # reincia contador para nuevo analisis
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[1] = 0
                    regC[1] = 0


        elif (theta > 90 and theta < 136):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt2[regC[2]] = r
            regC[2] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 135:
                average[2] = sum(pnt2) / len(pnt2)
                if average[2] < 40:
                    movlog[2] = 1
                    regC[2] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[2] = 0
                    regC[2] = 0

        elif (theta > 135 and theta < 181):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt3[regC[3]] = r
            regC[3] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 180:
                average[3] = sum(pnt3) / len(pnt3)
                if average[3] < 40:
                    movlog[3] = 1
                    regC[3] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog[3] = 0
                    regC[3] = 0

        elif theta == 180:
            # decision de movimiento:
            rmov[0] = str(movlog[0]) + str(movlog[1]) + str(movlog[2]) + str(movlog[3])
            print(rmov[0])
            idle[0] = 1  # identificador de que se completo el analisis en ccw


############################################################                        
    elif dire == "cw":
        if (theta > 170 and theta < 136):  # check
            # cantidad de puntos [para realizar el promedio]
            pnt0_cw[regC_cw[0]] = r
            regC_cw[0] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 135:
                average_cw[0] = sum(pnt0_cw) / len(pnt0_cw)
                if average_cw[0] < 40:
                    movlog_cw[3] = 1
                    regC_cw[0] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog_cw[3] = 0
                    regC_cw[0] = 0

        elif (theta > 134 and theta < 91): #check
            # cantidad de puntos [para realizar el promedio]
            pnt1_cw[regC_cw[1]] = r
            regC_cw[1] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 90:
                average_cw[1]=sum(pnt1_Cw)/len(pnt1_Cw)
                if average_cw[1] <40:
                    movlog_cw[2] = 1
                    regC_cw[1] = 1
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog_cw[2] = 0
                    regC_cw[1] = 1

        elif (theta > 89 and theta < 46): #check
            # cantidad de puntos [para realizar el promedio]
            pnt2[regC_cw[2]] = r
            regC_cw[2] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 45:
               average_cw[2]=sum(pnt2_cw)/len(pnt2_cw)
                if average_cw[2] <40:
                    movlog_cw[1] = 1
                    regC_cw[2] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog_cw[1] = 0
                    regC_cw[2] = 0

        elif (theta < 46): #check
            # cantidad de puntos [para realizar el promedio]
            pnt3[regC_cw[3]] = r
            regC_cw[3] += 1
            # promedio de distancia[max dist 38cm]
            if theta == 180:
                average_cw[3]=sum(pnt3_cw)/len(pnt3_cw)
                if prom < 40:
                    movlog_cw[0] = 1
                    regC_cw[3] = 0
                else:
                    # obstaculo logico[1=pared, 0=libre]
                    movlog_cw[0] = 0
                    regC_cw[3] = 0

        elif theta == 0:
            # decision de movimiento:
            rmov[1] = str(movlog[3]) + str(movlog[2]) + str(movlog[1]) + str(movlog[0])
            idle[1] = 1

    elif idle[0] * idle[1] == 1:
        print(rmov[0] + rmov[1])
        if rmov[0] == rmov[1]:
            if mov == "1001":
                # avanzar recto
                idle[0] = 0
                idle[1] = 0
                return ('w',0)

            if mov == "0001":
                # avanzar izquierda 90 grados
                idle[0] = 0
                idle[1] = 0
                return ('a',0)

            if mov == "1000":
                # avanzar derecha 90 grados
                idle[0] = 0
                idle[1] = 0
                return ('d',0)

            if mov == "1111":
                # rotar 180
                idle[0] = 0
                idle[1] = 0
                return ('q',0)

        else:
            return ('x', 1)
            print("mapeando")
######################################

