from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import socket
import collections
import math
import numpy as np

class DynamicPlotter():

    def __init__(self, sampleinterval=0.1, timewindow=10., size=(640,480)):
        # Data stuff
        self._interval = int(sampleinterval*1000) #coloca al intervalo en ms
        self._bufsize = int(timewindow/sampleinterval)#recibire maximo 351 puntos del radar
        self.databufferx = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.databuffery = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-30., 30., self._bufsize) #esto se mantiene
        self.y = np.zeros(self._bufsize, dtype=np.float)
        # PyQtGraph stuff
        self.app = QtGui.QApplication([])
        self.plt = pg.plot(title='reg0-180 [PyQtGraph]')
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setXRange(-30,30)
        self.plt.setYRange(0,45)
        #self.plt.setLabel('left', 'Distancia horizontal con respecto al sensor', 'cm')
        #self.plt.setLabel('bottom', 'Distancia vertical', 'cm')
        self.radar = self.plt.plot(self.x, self.y, pen=None,symbol='o')

        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def updateplot(self):
        data = s.recv(12)

        print(data)
        if data == '1':
            self.app.closeAllWindows()
        data_decode=data.decode("utf-8")
        data_str=str(data_decode)
        packet_slice=data_str.partition('s')
        deg,distance=packet_slice[0].split(",")
        deg=float(deg)
        distance=float(distance)
        if(deg<171):
            rectx=distance*math.cos(math.radians(deg))
            recty=distance*math.sin(math.radians(deg))

            self.databufferx.append(rectx)
            self.databuffery.append(recty)

            self.x[:] = self.databufferx
            self.y[:] = self.databuffery

            self.radar.setData(self.x, self.y,pen=None,symbol='o')
        if(deg==169):
            self.databufferx = collections.deque([0.0]*self._bufsize, self._bufsize)
            self.databuffery = collections.deque([0.0]*self._bufsize, self._bufsize)

        self.app.processEvents()

    def run(self):
        self.app.exec_()

if __name__ == '__main__':

    server_address = ('192.168.43.105',6794)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    m = DynamicPlotter(sampleinterval=0.0001, timewindow=0.0351) #intervalo en segundos
    m.run()
