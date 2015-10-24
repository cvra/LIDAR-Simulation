import collections, random, time, math, sys
import numpy as np
import matplotlib.path as mplPath
from hull import convex_hull

class RectangleInfo():
	def __init__(self, points, dim, angle):
		self.points = points
		self.dim = dim
		self.angle = angle


class MinimumAreaRectangle():

	def findExtrema(self, cloud):
		''' cloud is numpy.ndarray'''
	  	maxs = np.argmax(cloud, axis=0)
	  	mins = np.argmin(cloud, axis=0)
	  	Index = np.concatenate((maxs, mins),axis=0)
	  	extremaPts = cloud[Index,:]
		return extremaPts
    
	def keepPtsOutsideBox(self, cloud, polygon):
		ppPath = mplPath.Path(polygon)
		ind = ppPath.contains_points(cloud)
		return cloud[~ind]

	def compute2DconvexHulls(self, cloud):
	  	convexHulls = convex_hull(cloud.tolist())
	  	return np.array(convexHulls)

	def rotatePolygon(self, polygon,theta):
		cosTheta = math.cos(theta)
		sinTheta = math.sin(theta)
		rotMat = np.asmatrix([[cosTheta, -sinTheta],[sinTheta, cosTheta]])
		return np.dot(rotMat, polygon.T).T

	def minimumAreaRectangle(self, polygon):
		areaMin = sys.float_info.max
		minRectangle = RectangleInfo(np.array([[0, 0], [0, 0]]), 0, 0) 

		for i in range(0, polygon.shape[0]):
			diff = polygon[i,:] - polygon[i-1,:]
			omega = math.atan2(diff[1], diff[0])
			rotPolygon = self.rotatePolygon(polygon, -omega)
			rotPolygon = np.asarray(rotPolygon)

			extremas = self.findExtrema(rotPolygon)

			trCorner = np.amax(extremas,axis=0)
			blCorner = np.amin(extremas,axis=0)
			tlCorner = np.array([blCorner[0], trCorner[1]])
			brCorner = np.array([trCorner[0], blCorner[1]])

			rectangleSize = trCorner - blCorner

			area = np.prod(rectangleSize)

			if area < areaMin:
				areaMin = area

				rect = np.array([blCorner, brCorner, trCorner, tlCorner])
				rect = self.rotatePolygon(rect, omega)
				rect = np.asarray(rect)

				minRectangle.points = rect
				minRectangle.dim = rectangleSize
				minRectangle.angle = omega

		return minRectangle


