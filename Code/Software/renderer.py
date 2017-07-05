import pygame, math
import time

class Renderer():
	def __init__(self, WindowRes):
		self.WindowRes = WindowRes
		self.MAXRANGE = 600 # max range to be drawn in cm

		self.screencenter = (self.WindowRes[0] / 2, self.WindowRes[1] / 2)
		self.workable_area = min(self.WindowRes[0] - 10, self.WindowRes[1] - 10)

		self.density = (self.workable_area / 2) / float(self.MAXRANGE) # cm/pixel

		

	def Draw(self, window, points):
		self.draw_guidelines(window)

		self.draw_points(window, points)

		

	def draw_guidelines(self, window):
		pygame.draw.line(window, (255, 255, 255), 
			(0, self.WindowRes[1] / 2), 
			(self.WindowRes[0], self.WindowRes[1] / 2), 1)

		pygame.draw.line(window, (255, 255, 255), 
			(self.WindowRes[0] / 2, 0), 
			(self.WindowRes[0] / 2, self.WindowRes[1]), 1)



		

		n_circles = 3
		for i in range(1, n_circles + 1):
			pygame.draw.circle(window, (255, 255, 255), self.screencenter, (self.workable_area / 2) * i/n_circles, 1)

	def draw_points(self, window, points):
		for point in points:
			a = math.radians(point[0])
			r = self.density * point[1]

			if a < math.radians(360):
				position = (int(r * math.cos(a)), 
							int(r * math.sin(a)))

				color = (0, 255, 0)
				if point[1] < 60:
					color = (140, 0, 0)

				pygame.draw.circle(window, color, 
					(position[0] + self.screencenter[0], position[1] + self.screencenter[1]),
					2)