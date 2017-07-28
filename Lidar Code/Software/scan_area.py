'''
Calculates the area of the surface detected by the lidar
'''

class SurfaceCalculator():
	def SurfaceFromPoints(self, points):
		area = 0.0

		for i in range(len(points) - 1):
			area += points[i][0] * points[i+1][1]
		area += points[-1][0] * points[0][1]

		for i in range(len(points) - 1):
			area -= points[i+1][0] * points[i][1]
		area -= points[0][0] * points[-1][3]
		return area / 2.0


calculator = SurfaceCalculator()
print calculator.SurfaceFromPoints([(2, 1), (4, 5), (7, 8)])