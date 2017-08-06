import math

# Reference : https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm
# Demo      : https://www.youtube.com/watch?v=cPZK_FpCMy8
'''
The purpose of the algorithm is, given a curve composed of line segments, to find a similar curve with fewer points.
Tolerance controls how refined the result will be (low tolerance -> more lines)
'''

def DouglasPeucker(points, tolerance = 20):
	dmax = 0.0
	index = 0

	for i in xrange(1, len(points)):
		d = distance_point_to_line(points[i], points[0], points[-1])
		if d > dmax:
			index = i
			dmax = d

	if dmax > tolerance:
		recResults1 = DouglasPeucker(points[:index], tolerance)
		recResults2 = DouglasPeucker(points[index:], tolerance)

		result = recResults1[:] + recResults2
	else:
		result = [(points[0], points[-1])]
	return result




def distance_point_to_line(point, p1, p2):
		# we are given a line defined by two points
		# calculate the distance (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
		try:
			return float(abs((p2[1] - p1[1])*point[0] - (p2[0] - p1[0])*point[1] + p2[0]*p1[1] - p2[1]*p1[0]) / float(math.sqrt( (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)))
		except ZeroDivisionError:
			return 0.0 # if points are at the exact same pos, it won't divide by 0 ==> manually give 0 distance


# test function
#print DouglasPeucker([(0,0), (4,12), (8,0)])