import math

class Analyser():
	def __init(self):
		pass

	def FindLines(self, points, threshold):
		pass


	def FindLinearTendency(self, points):
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

		R2 = sxy / (sx * sy)

		# The formula gives us : y - moy_y = a(x - moy_x)
		# ==> y = ax + (moy_y - a*moy_x)
		a = sxy / vx
		b = moy_y - a * moy_x

		#returns a, b from y = ax + b and R^2
		return a, b, R2