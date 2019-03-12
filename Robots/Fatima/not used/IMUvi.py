#!/usr/bin/env python

from pyglet.gl import *
import ctypes
import sys
from pywavefront import visualization
import pywavefront

sys.path.append('..')
rotationx = 0
rotationy = 0
rotationz = 0
meshes = pywavefront.Wavefront('data/CUBE.obj')
window = pyglet.window.Window()
lightfv = ctypes.c_float * 4


@window.event
def on_resize(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(1.0, 0.0, 1.0, 0.0)) #Posicion de la iluminacion
    glEnable(GL_LIGHT0)
    glClearColor(1,1,1,0)
    glTranslated(0.0, 0.0, -5.0)
    
    # rotacion sobre ejes x,y,z
    #glRotatef(0, 0.0, 0.0, 0.0) #Rotacion sobre eje x
    #glRotatef(rotationy, 0.0, 1.0, 0.0) #Rotacion sobre eje y
    #glRotatef(rotationz, 0.0, 0.0, 1.0) #Rotacion sobre eje z

    glEnable(GL_LIGHTING)
    visualization.draw(meshes)




#def update(dt):
    #global rotationx
    #global rotationy
    #global rotationz
    #Recibo los valores de cuando se lee el puerto serial del script mazedist.py(usando queque)
    #los almaceno en las variables rotatex rotatey rotatez
    # y ya ._. (khe easy)
    #esto sucedera cada 16 ms


#pyglet.clock.schedule(update)
pyglet.app.run()
