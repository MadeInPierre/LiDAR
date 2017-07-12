import math

class Analyser():
	def __init(self):
		pass

	def FindLines(self, points, threshold = 0.99):
		lines = [] # line is defined by it's first and last point
		
		i = 0
		while i < len(points) - 4:
			'''
			TODO wrap around i = len and i = 0
			Start with the 4 points after <p_i>.
				- If a line is detected, try to see is there's still a line with the next 5 points.
				- If not, the line is ended.
			'''
			# Searching = True
			# FoundLine = False
			# line_length = 4 # PARAM initial minimal line length

			# while Searching:
			# 	if self.FindLinearTrendline(points[i : i + line_length], threshold)[0] == True:
			# 		FoundLine = True
					
			# 		if i + 1 < len(points):
			# 			i += 1
			# 	else:
			# 		pass






			found_line = False
			line_length = 4 
			while self.FindLinearTrendline(points[i : i + line_length], threshold)[0] == True and i + line_length < len(points): #grow the line untile it isn't a line anymore
				found_line = True
				line_length += 1

			if found_line:
				line_length -= 1
				lines.append((i, i + line_length))
				i = i + line_length
			else:
				i += 1
		return lines


	def FindLinearTrendline(self, points, threshold = 0.73):
		try:
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

			#returns a, b from y = ax + b and R^2
			return True if R2 > threshold else False, a, b, R2
		except:
			return None, None, None, None

