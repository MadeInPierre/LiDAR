import math
from DouglasPeucker import * # line finder function

class Analyser():
	def __init(self):
		pass

	def FindWalls(self, points, precision_limit):
		print "finding walls"
		TOLERANCE = 12.0
		MIN_LENGTH = 6   # Min wall length in cm

		lines = DouglasPeucker(points, tolerance = TOLERANCE) # reduce 

		#remove lines that include points too close to lidar (poor precision)
		lines = [line for line in lines if (self.distance_point_to_point((0,0), line[0]) >= precision_limit and \
											self.distance_point_to_point((0,0), line[1]) >= precision_limit)]


		result = []
		for l in lines:
			#wall_size = math.sqrt((l[1][1] - l[0][1])**2 + (l[1][0] - l[0][0])**2) # sqrt[ (yb - ya)^2 + (xb - xa)^2 ]
			if l[2] >= MIN_LENGTH:
				result.append(l)

		return result








		'''
		>> THE CODE THAT FOLLOW IS USELESS. KEPT JUST IN CASE FOR NOW ONLY. <<
		'''















		lines = [] # line is defined by it's first and last point
		
		i = 0
		while i < len(points):
			'''
			TODO wrap around i = len and i = 0

			Start with the 4 points after <p_i>.
				- If a line is detected, try to see is there's still a line with the next 5 points. Reapeat the step.
				- If not, the line is ended.
			'''
			MIN_POINTS = 6 # start with 4 points minimum for a line


			line_length = MIN_POINTS



			Searching = True
			while Searching:
				if i + line_length < len(points):
					if self.is_line(points[i : i + line_length]) > 0:
						line_length += 1
					else:
						Searching = False
				else:
					line_length = len(points) - 1 - i
					Searching = False



			if line_length > MIN_POINTS:
				p1, p2, strength = self.FindLinearTrendline(points[i: i + line_length - 1])
				#if (abs(p1[0]) < 25 and abs(p1[1]) < 25) or (abs(p2[0]) < 25 and abs(p2[1]) < 25):
				#	print "LINE REJECTED" #TEMPORARY reject lines that pass by the center (they are noise)
				#else:
				lines.append((p1, p2, strength))
				i += line_length
			else:
				i += 1


		return lines


	def is_line(self, points):
		#returns a strength float score from 0 fo 1 (0 = no line)
		#a, b = self.line_from_twopoints(points[0], points[-1])

		i = 0
		for point in points:
			dist_to_line = self.distance_point_to_line(point, points[0], points[-1])
			dist_to_center = math.sqrt(point[0]**2 + point[1]**2)

			#TOLERANCES
			if dist_to_center < 30:
				tol = 0.0
			elif dist_to_center < 100:
				tol = 6
			elif dist_to_center < 300:
				tol = 18
			elif dist_to_center < 500:
				tol = 22
			elif dist_to_center < 1000:
				tol = 34
			elif dist_to_center < 40000:
				tol = 40
			else:
				print dist_to_center

			tol = tol / 2.0 if i < 5 else tol # small lines have less tolerance
			if point[0] != 0 and point[1] != 0:
				if dist_to_line > tol:
					return 0
			i += 1

		return 1

	'''
	def line_from_twopoints(self, p1, p2):
		# y = ax + b

		a = (p2[1] - p1[1]) / (p2[0] - p1[0])
		b = p1[1] - a * p1[0]
		return a, b

	def distance_point_to_line(self, point, a, b):
		# we are given a line defined by y = ax + b
		# the formula we use needs cx + dy + e = 0 ==> -ax + y - b = 0
		c = -a
		d = 1
		e = -b

		# calculate the distance (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
		distance = abs(c * point[0] + d * point[1] + e) / math.sqrt(c**2 + d**2)
		return distance
	'''
	def distance_point_to_point(self, p1, p2):
		return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2) # sqrt[ (yb - ya)^2 + (xb - xa)^2 ]

	def distance_point_to_line(self, point, p1, p2):
		# we are given a line defined by two points
		# calculate the distance (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
		try:
			return abs((p2[1] - p1[1])*point[0] - (p2[0] - p1[0])*point[1] + p2[0]*p1[1] - p2[1]*p1[0]) / float(math.sqrt( (p2[1] - p1[1])**2 + (p2[0] - p1[0])**2))
		except:
			return 0.0 # if points are at the exact same pos, it won't divide by 0 ==> manually give 0 distance

	def FindLinearTrendline(self, points):
		# implementation of https://www.youtube.com/watch?v=BeGKpJNCdf0
		# y = ax + b

		S_x   = 0.0 # S = Sigma (sum)
		S_y   = 0.0
		S_x2  = 0.0
		S_y2  = 0.0
		S_xy  = 0.0

		for p in points:
			xi, yi = p[0], p[1]

			S_x += xi
			S_y += yi

			S_x2 += xi**2
			S_y2 += yi**2

			S_xy += xi * yi

		N = len(points)
		moy_x = S_x / N
		moy_y = S_y / N

		vx = (S_x2/N) - moy_x**2
		vy = (S_y2/N) - moy_y**2

		sx = math.sqrt(vx)
		sy = math.sqrt(vy)
		sxy = S_xy/N - moy_x * moy_y

		R2 = (sxy / (sx * sy))**2

		# The formula gives us : y - moy_y = a(x - moy_x)
		# ==> y = ax + (moy_y - a*moy_x)
		a = sxy / vx
		b = moy_y - a * moy_x
		# we have y = ax + b

		# Now we find the start and end point of the line
		# (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
		# we have an equation of type = ax + b, we need ax + by + c = 0
		c = -a
		d = 1
		e = -b

		start_point_x = (d*( d*points[0][0]  - c*points[0][1] ) - c*e) / (c**2 + d**2)
		start_point_y = (c*(-d*points[0][0]  + c*points[0][1] ) - d*e) / (c**2 + d**2)

		end_point_x   = (d*( d*points[-1][0] - c*points[-1][1]) - c*e) / (c**2 + d**2)
		end_point_y   = (c*(-d*points[-1][0] + c*points[-1][1]) - d*e) / (c**2 + d**2)

		'''
		# Now we find the start and end point of the line
		first_point_line_coeff = points[0][1] / points[0][0]
		start_point_x = b / (first_point_line_coeff - a)
		start_point_y = a * start_point_x + b

		last_point_line_coeff = points[-1][1] / points[-1][0]                     
		end_point_x = b / (last_point_line_coeff - a)
		end_point_y = a * end_point_x + b
		'''
		return (start_point_x, start_point_y), (end_point_x, end_point_y), R2