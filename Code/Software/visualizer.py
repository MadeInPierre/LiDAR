import pygame
from renderer import Renderer
from serial_manager import *



def update_points(points, new_points):
	if new_points is not None:
		for p in new_points:
			points.insert(0, p)
		try:
			del points[360:]
		except:
			print("EXCEPTION")
			pass

		return points
	else:
		return points




pygame.init()
clock = pygame.time.Clock()

WindowRes = (800, 600)
window = pygame.display.set_mode(WindowRes)
pygame.display.set_caption("LIDAR Cloud POV")

renderer = Renderer(WindowRes)
serial = SerialManager("COM6", 115200)
serial.openSerial()

points = []

running = True
while running:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False

	window.fill((0, 0, 0))

	serial_update = serial.getSerialInput()
	#points = points if serial_update == None else serial_update
	points = update_points(points, serial_update)
	
	renderer.Draw(window, points)

	pygame.display.update()
	clock.tick(20)

pygame.quit()
serial.closeSerial()
quit()


