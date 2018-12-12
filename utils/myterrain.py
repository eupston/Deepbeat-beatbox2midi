import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import sys
from opensimplex import OpenSimplex
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import time

class Terrain(object):
    def __init__(self):
        """
        Initialize the graphics window and mesh
        """

        # setup the view window
        self.w = gl.GLViewWidget()

        # self.w.setGeometry(0, 110, 1000, 1000)
        self.w.setCameraPosition(distance=30, elevation=10)


        self.w.setWindowFlags(Qt.FramelessWindowHint)
        self.w.setAttribute(Qt.WA_TranslucentBackground, True)
        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)



        # constants and arrays
        self.nsteps = 1
        self.ypoints = range(-20, 22, self.nsteps)
        self.xpoints = range(-20, 22, self.nsteps)
        self.nfaces = len(self.ypoints)
        self.offset = 0

        # perlin noise object
        self.tmp = OpenSimplex()

        # create the veritices array
        verts = np.array([
            [
                x, y, 1.5 * self.tmp.noise2d(x=n / 5, y=m / 5)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        # create the faces and colors arrays
        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                colors.append([0, 0, 0, 0])
                colors.append([0, 0, 0, 0])

        faces = np.array(faces)
        colors = np.array(colors)

        # create the mesh item
        self.m1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces, faceColors=colors,
            smooth=False, drawEdges=False,
        )
        # self.m1.setGLOptions('opaque')
        self.m1.setGLOptions('additive')
        self.w.addItem(self.m1)




    def getwidget(self):
        return self.w


    def update(self):
        """
        update the mesh and shift the noise each time
        """
        verts = np.array([
            [
                x, y, 2.5 * self.tmp.noise2d(x=n / 5 + self.offset, y=m / 5 + self.offset)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])
                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.8])

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        self.m1.setMeshData(
            vertexes=verts, faces=faces, faceColors=colors
        )
        self.offset -= 0.10


    def animate(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)


    def stop_animate(self):
        self.timer.stop()