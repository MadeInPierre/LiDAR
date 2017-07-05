import pygame, math
import time

class Renderer():
	def __init__(self, WindowRes):
		self.WindowRes = WindowRes
		self.MAXRANGE = 500 # max range to be drawn in cm
		self.PRECISION_LIMIT = 50

		self.screencenter = (self.WindowRes[0] / 2, self.WindowRes[1] / 2)
		self.workable_area = min(self.WindowRes[0] - 10, self.WindowRes[1] - 10)

		self.density = (self.workable_area / 2) / float(self.MAXRANGE) # cm/pixel

		

	def Draw(self, window, lap):
		window.fill((20, 20, 20))

		self.draw_guidelines(window)

		if lap is not None:
			self.draw_points(window, lap)

		

	def draw_guidelines(self, window):
		pygame.draw.line(window, (150, 150, 150), 
			(0, self.WindowRes[1] / 2), 
			(self.WindowRes[0], self.WindowRes[1] / 2), 1)

		pygame.draw.line(window, (150, 150, 150), 
			(self.WindowRes[0] / 2, 0), 
			(self.WindowRes[0] / 2, self.WindowRes[1]), 1)



		

		n_circles = 3
		for i in range(1, n_circles + 1):
			pygame.draw.circle(window, (180, 180, 180), self.screencenter, (self.workable_area / 2) * i/n_circles, 1)

	def draw_points(self, window, lap):
		for point in lap.getPoints():
			a = math.radians(point[0] + 90)
			r = self.density * point[1]

			position = (int(r * math.cos(a)), int(r * math.sin(a)))
			final_position = (self.screencenter[0] + position[0], self.screencenter[1] - position[1])

			point_color = (0, 255, 0)
			if point[1] < self.PRECISION_LIMIT:
				point_color = (140, 0, 0)

				limit_r = min(self.PRECISION_LIMIT, point[1])
				precision_limit_position = (self.density * limit_r * math.cos(a), self.density * limit_r * math.sin(a))
				precision_final_position = (self.screencenter[0] + precision_limit_position[0], self.screencenter[1] - precision_limit_position[1])
				pygame.draw.line(window, (30, 0, 0), self.screencenter, precision_final_position, 4)
			else:
				pygame.draw.line(window, (0, 60, 0), self.screencenter, final_position, 4)

			pygame.draw.circle(window, (point_color), final_position, 4)