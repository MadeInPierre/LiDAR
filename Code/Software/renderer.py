import pygame, math
import time

class Renderer():
	def __init__(self, WindowRes):
		self.WindowRes = WindowRes
		self.PRECISION_LIMIT = 50

		self.screencenter = (self.WindowRes[0] / 2, self.WindowRes[1] / 2)
		self.workable_area = min(self.WindowRes[0] - 10, self.WindowRes[1] - 10)

		self.update_zoom(800)


		self.font = pygame.font.SysFont("Arial", 60)
		self.font2 = pygame.font.SysFont("Arial", 20)

	def update_zoom(self, max_range):
		self.MAXRANGE = max_range # max range to be drawn in cm
		self.density = (self.workable_area / 2) / float(self.MAXRANGE) # cm/pixel
		print "zoom" + str(self.MAXRANGE)


	def Zoom(self):
		self.update_zoom(self.MAXRANGE + 50)
	def UnZoom(self):
		self.update_zoom(self.MAXRANGE - 50)

		

	def Draw(self, window, lap_stack):
		window.fill((20, 20, 20))

		self.draw_guidelines(window)

		if lap_stack is not None and lap_stack.getNumberOfLaps() > 0:
			self.draw_points(window, lap_stack.getLatestLap())
			self.draw_gui(window, lap_stack)


		

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


		for point in lap.getPoints():
			a = math.radians(point[0] + 90)
			r = self.density * point[1]

			point_color = (0, 255, 0)
			if point[1] < self.PRECISION_LIMIT:
				point_color = (140, 0, 0)

			position = (int(r * math.cos(a)), int(r * math.sin(a)))
			final_position = (self.screencenter[0] + position[0], self.screencenter[1] - position[1])
			pygame.draw.circle(window, (point_color), final_position, 3)

	def draw_gui(self, window, lap_stack):
		speed_canvas = pygame.Surface((225, 100))
		speed_canvas.fill((80, 80, 80))
		window.blit(speed_canvas, (0, 0))

		hz = '%.2f' % lap_stack.getLastHz()
		Hz_text = self.font.render(hz + " Hz", True, (255, 255, 255))
		window.blit(Hz_text, (10, 3))

		speed_text = self.font2.render("Speed Level : " + str(lap_stack.CurrentLidarSpeed), True, (255, 255, 255))
		window.blit(speed_text, (45, 68))	


		range_text = self.font2.render(str(self.MAXRANGE) + "m", True, (255, 255, 255))
		window.blit(range_text, (self.workable_area - range_text.get_width(), self.screencenter[1] - 23))		