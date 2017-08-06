import pygame, math
import time
from analyser import *

class Renderer():
	def __init__(self, WindowRes):
		self.WindowRes = WindowRes

		self.screencenter = (self.WindowRes[0] / 2, self.WindowRes[1] / 2)
		self.workable_area = min(self.WindowRes[0] - 10, self.WindowRes[1] - 10)

		self.update_zoom(800)


		self.font = pygame.font.SysFont("Arial", 60)
		self.font2 = pygame.font.SysFont("Arial", 20)

		self.SHOW_WALLS = True
		self.SHOW_POINTS = True

	def toggleWalls(self):
		self.SHOW_WALLS = not self.SHOW_WALLS
	def togglePoints(self):
		self.SHOW_POINTS = not self.SHOW_POINTS


	def update_zoom(self, max_range):
		self.MAXRANGE = max_range # max range to be drawn in cm
		self.density = (self.workable_area / 2) / float(self.MAXRANGE) # cm/pixel

	def Zoom(self):
		self.update_zoom(self.MAXRANGE + 50)
	def UnZoom(self):
		self.update_zoom(self.MAXRANGE - 50)

		

	def Draw(self, window, lap_stack, analyser):
		window.fill((20, 20, 20))

		self.draw_guidelines(window)

		if lap_stack is not None and lap_stack.getNumberOfLaps() > 0:
			if self.SHOW_POINTS:
				self.draw_points(window, lap_stack.getLastLap())
				#self.draw_linearmode(window, lap_stack)
			if self.SHOW_WALLS:
				self.draw_lines(window, lap_stack, analyser)

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
		for point in lap.getPointsPolar():
			pos = self.pointPolarToMap(point)

			color = (0, 60, 0)
			if point[1] < lap.PRECISION_LIMIT:
				color = (60, 0, 0)

			pygame.draw.line(window, color, self.screencenter, pos, 4)

		for point in lap.getPointsPolar():
			pos = self.pointPolarToMap(point)

			color = (0, 255, 0)
			if point[1] < lap.PRECISION_LIMIT:
				color = (140, 0, 0)

			pygame.draw.circle(window, (color), pos, 3)

	def draw_gui(self, window, lap_stack):
		speed_canvas = pygame.Surface((225, 100))
		speed_canvas.fill((80, 80, 80))
		window.blit(speed_canvas, (0, 0))

		hz = '%.2f' % lap_stack.getLastHz()
		Hz_text = self.font.render(hz + " Hz", True, (255, 255, 255))
		window.blit(Hz_text, (10, 3))

		speed_text = self.font2.render("Speed Level : " + str(lap_stack.CurrentLidarSpeed), True, (255, 255, 255))
		window.blit(speed_text, (45, 68))	


		range_text = self.font2.render(str(self.MAXRANGE) + "cm", True, (255, 255, 255))
		window.blit(range_text, (self.workable_area - range_text.get_width(), self.screencenter[1] - 23))		

	def draw_lines(self, window, lap_stack, analyser):
		lines = analyser.FindWalls(lap_stack.getLastLap().getPointsCartesian(), lap_stack.getPrecisionLimit())
		for line in lines:
			print line
			pygame.draw.line(window, (255, 0, 0), self.pointCartesianToMap(line[0]), self.pointCartesianToMap(line[1]), 4)
				#self.pointPolarToMap(lap_stack.getLastLap().getPointsPolar()[line[0]]), 
				#									  self.pointPolarToMap(lap_stack.getLastLap().getPointsPolar()[line[1]]))


	def pointPolarToMap(self, point):
		a = math.radians(point[0] + 90)
		r = self.density * point[1]

		position = (int(r * math.cos(a)), int(r * math.sin(a)))
		map_position = (self.screencenter[0] + position[0], self.screencenter[1] - position[1])
		return map_position

	def pointCartesianToMap(self, point):
		if point[0] == 0:
			a = math.pi/2.0 if point[1] > 0 else -math.pi/2.0
		else:
			a = math.atan2(point[1], point[0])
		a += math.pi / 2.0
		r = math.sqrt(point[0]**2 + point[1]**2) * self.density
		
		position = (int(r * math.cos(a)), int(r * math.sin(a)))
		map_position = (self.screencenter[0] + position[0], self.screencenter[1] - position[1])
		return map_position



	def draw_linearmode(self, window, lap_stack):
		lap_points = lap_stack.getLastLap().getPointsPolar()

		x_interval = window.get_width() / len(lap_points)
		i = 0
		for point in lap_points:
			r = point[1]
			pygame.draw.circle(window, (255, 255, 0), (int(i * x_interval), window.get_height() - int(r * self.density)), 3)
			i += 1





	# def cartToPolar(self, point_xy)
	# 	point_polar = (point_xy[0] * math.cos(point_xy[0]), point_xy[1] * math.sin(point_xy[1]))
	# 	return point_polar