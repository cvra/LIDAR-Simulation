import collections, math, sys
import numpy as np
import matplotlib.path as mplPath

from hull import convex_hull
from rectangle import RectangleInfo

THRESHOLD_ALPHA = 0.3 
THRESHOLD_BETA  = 0.3 * 0.25
THRESHOLD_GAMMA = 0.3 * 0.4


def findExtrema(cloud):
	''' cloud is numpy.ndarray 
		return: bottom right top left
		(the same point can be returned several time)'''
  	maxs = np.argmax(cloud, axis=0)
  	mins = np.argmin(cloud, axis=0)
  	Index = [mins[1],maxs[1],maxs[0],mins[0]]
  	extremaPts = cloud[Index,:]
	return extremaPts

def keepPtsOutsideBox(cloud, polygon):
	ppPath = mplPath.Path(polygon)
	ind = ppPath.contains_points(cloud)
	return cloud[~ind]

def compute2DconvexHulls(cloud):
  	convexHulls = convex_hull(cloud.tolist())
  	return np.array(convexHulls)

def isCollinear(a, b, c, epsilon):
	if abs(np.cross(b-a, c-a)) < epsilon * np.linalg.norm(b-a):
		return True
	else:
		return False

def removeCollinearPts(polygon, epsilon):
	i = 0
	while i < polygon.shape[0] - 1:
		if isCollinear(polygon[i,:], polygon[i-2,:], polygon[i-1,:], epsilon):
			polygon = np.delete(polygon, i - 1, 0)
		else:
			i += 1
	return polygon


def rotatePolygon(polygon,theta):
	cosTheta = math.cos(theta)
	sinTheta = math.sin(theta)
	rotMat = np.asmatrix([[cosTheta, -sinTheta],[sinTheta, cosTheta]])
	return np.asarray(np.dot(rotMat, polygon.T).T)

def isRecangleValide(corners, hulls):
	ptsPerSide = [0, 0, 0, 0]

	for i in range(0, 4):
		for j in range(0, hulls.shape[0]):
			if isCollinear(corners[i,:], corners[i-1,:], hulls[j,:], 0.025):
				ptsPerSide[i] += 1

	if sum(ptsPerSide) < hulls.shape[0] * THRESHOLD_ALPHA:
		return False

	if sorted(ptsPerSide)[-2] < hulls.shape[0] * THRESHOLD_BETA:
		if sum(sorted(ptsPerSide)[-3:-1]) < hulls.shape[0] * THRESHOLD_GAMMA:
			return False


	return True

def minimumAreaRectangle(polygon, fullHulls):
	areaMin = sys.float_info.max
	bestRectangle = RectangleInfo(np.zeros([4, 2])) 
	rectangle = RectangleInfo(np.zeros([4, 2])) 

	for i in range(0, polygon.shape[0]):
		diff = polygon[i,:] - polygon[i-1,:]
		omega = math.atan2(diff[1], diff[0])
		rotPolygon = rotatePolygon(polygon, -omega)

		extremas = findExtrema(rotPolygon)

		trCorner = np.amax(extremas,axis=0)
		blCorner = np.amin(extremas,axis=0)
		tlCorner = np.array([blCorner[0], trCorner[1]])
		brCorner = np.array([trCorner[0], blCorner[1]])

		rectangleSize = trCorner - blCorner

		area = np.prod(rectangleSize)

		if area < areaMin:
			rect = np.array([blCorner, brCorner, trCorner, tlCorner])
			rect = rotatePolygon(rect, omega)

			rectangle.corners = rect

			if isRecangleValide(rect, fullHulls):
				areaMin = area
				bestRectangle.corners = rect

	return bestRectangle

class Positioning(object):

	def __init__(self, lidarPts=np.zeros([1, 2]), estimatedPos=np.zeros([1, 2])):
		self.lidarPts = lidarPts
		self.estimatedPos = estimatedPos

	@property
	def lidarPts(self):
		return self._points

	@lidarPts.setter
	def lidarPts(self, value):
		self._lidarPts = value
		self._computePos()

	@property
	def estimatedPos(self):
		return self._points

	@estimatedPos.setter
	def estimatedPos(self, value):
		self._pestimatedPos = value

	@property
	def minimalHulls(self):
		return self._minimalHulls

	@property
	def rectangle(self):
		return self._rectangle

	def _computePos(self):
		hulls = compute2DconvexHulls(self._lidarPts)
		cleanHulls = removeCollinearPts(hulls, 0.02);
		self._minimalHulls = cleanHulls
		self._rectangle =  minimumAreaRectangle(cleanHulls, self._lidarPts)

