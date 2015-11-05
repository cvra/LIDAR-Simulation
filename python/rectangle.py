import collections, math
import numpy as np

X = 0
Y = 1

class RectangleInfo(object):

	def __init__(self, points=np.zeros([4, 2])):
		''' points: 2x4 np.array'''
		self._corners = None
		self._size = None
		self._angle = None
		self._permutation = [None] * 4
		self.corners = points
	
	@property
	def corners(self):
		return self._corners

	@corners.setter
	def corners(self, value):
		mins = np.amin(value, axis=0)
		maxs = np.amax(value, axis=0)

		self._corners = []

		ind = np.where(value[:, Y] == mins[Y])[0]
		ind = ind[np.argmin(value[ind, X], axis=0)]
		self._corners.append(value[ind])
		self._permutation[0] = ind

		ind = np.where(value[:,X] == maxs[X])[0]
		ind = ind[np.argmin(value[ind,Y], axis=0)]
		self._corners = np.vstack((self._corners, value[ind]))
		self._permutation[1] = ind

		ind = np.where(value[:, Y] == maxs[Y])[0]
		ind = ind[np.argmax(value[ind, X], axis=0)]
		self._corners = np.vstack((self._corners, value[ind]))
		self._permutation[2] = ind

		ind = np.where(value[:,X] == mins[X])[0]
		ind = ind[np.argmax(value[ind,Y], axis=0)]
		self._corners = np.vstack((self._corners, value[ind]))
		self._permutation[3] = ind

		diff = self._corners[1] - self._corners[0]
		self._angle = math.atan2(diff[1], diff[0])

		self._size = [np.linalg.norm(self._corners[1]-self._corners[0]), np.linalg.norm(self._corners[-1]-self._corners[0])]

	@property
	def angle(self):
		return self._angle

	@property
	def size(self):
		return self._size

	@property
	def permutation(self):
		return self._permutation

