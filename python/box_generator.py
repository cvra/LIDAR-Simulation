import collections
import random
import time
import math
import numpy as np
import sys


sandbox_text_end = '''children [
    USE SANDBOX_SHAPE
  ]
  boundingObject USE SANDBOX_SHAPE
  physics Physics {
  }
}'''

nbCube = 24

posX = [random.uniform(0., 3.) for _ in range(0, nbCube)]
posY = [random.uniform(0.5, 0.2) for _ in range(0, nbCube)]
posZ = [random.uniform(0., 2.) for _ in range(0, nbCube)]


rotX = [random.uniform(0., 3.14) for _ in range(0, nbCube)]
rotY = [random.uniform(0., 3.14) for _ in range(0, nbCube)]
rotZ = [random.uniform(0., 3.14) for _ in range(0, nbCube)]
rotAngle = [random.uniform(0., 3.14) for _ in range(0, nbCube)]

for i in range(0, nbCube):
	print "DEF SANDBOX%d Solid{" % i
	print "  translation %.2f %.2f %.2f" % (posX[i], posY[i], posZ[i])
	print "  rotation %.2f %.2f %.2f %.2f" % (rotX[i], rotY[i], rotZ[i], rotAngle[i])
	print sandbox_text_end

