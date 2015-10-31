import SocketServer, socket, collections, math, json
import numpy as np

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from lidarProcessing import Positioning


# PyQtGraph stuff
app = QtGui.QApplication([])
pg.setConfigOptions(antialias=True)
plot = pg.plot(title='Lidar Polar Plot')
plot.resize(600,600)
plot.setAspectLocked()

lidarProcess = Positioning()

def PlotPolar():
    # Add polar grid lines
    plot.addLine(x=0, pen=0.2)
    plot.addLine(y=0, pen=0.2)

    radius = np.arange(0.2, 3, 0.2);
    for r in radius:
        circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r*2, r*2)
        circle.setPen(pg.mkPen(color=(30, 30, 30)))
        plot.addItem(circle)

    radius = np.arange(1, 3.1, 1);
    for r in radius:
        circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r*2, r*2)
        circle.setPen(pg.mkPen(color=(60, 60, 60)))
        plot.addItem(circle)
        plot.setXRange(-3, 3)
        plot.setYRange(-3, 3)


class MyUDPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()

        socket = self.request[1]
        socket.sendto(data.upper(), self.client_address)

        # compute polar coordinate
        radius = json.loads(data);
        radius = radius[::-1]

        theta = np.linspace(-0.436332313, np.pi+0.436332313, len(radius))

        # Transform to cartesian and plot
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)

        cloudPts = np.array([x, y]).T;

        plot.clear()
        PlotPolar()

        # draw raw measure
        linePen = pg.mkPen(color=(200, 200, 200, 200), width= 2, style=QtCore.Qt.DotLine)
        plot.plot(x, y, pen=linePen,  symbol='o', symbolPen=None, symbolSize=7, symbolBrush=(255, 234, 0, 160))
        
        lidarProcess.lidarPts = cloudPts

        # draw processed features
        plot.plot(lidarProcess.minimalHulls[:,0], lidarProcess.minimalHulls[:,1], pen=None,  symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(0, 255, 0, 200))
        plot.plot(lidarProcess.rectangle.corners[:,0], lidarProcess.rectangle.corners[:,1], pen=None,  symbol='x', symbolPen=None, symbolSize=15, symbolBrush=(255, 0, 0, 255))

        app.processEvents()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.socket.setsockopt( socket.SOL_SOCKET, socket.SO_RCVBUF, 64000)
    server.serve_forever()

