import pygame
from renderer import Renderer
from serial_manager import *




pygame.init()
clock = pygame.time.Clock()

WindowRes = (1600, 1600)
window = pygame.display.set_mode(WindowRes)
pygame.display.set_caption("LIDAR Cloud POV")

renderer = Renderer(WindowRes)
communication = SerialManager("/dev/ttyUSB0", 500000)
communication.openSerial()

PointsPerLap = communication.getPointsPerLap()
print("Got PPL = " + str(PointsPerLap))
lapsStack = LapsStack(PointsPerLap)

communication.resetLidar()


running = True
while running:
	events = pygame.event.get()
	for event in events: # quitting the program
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False




	serial_update = communication.updateSerial(lapsStack = lapsStack)
	
	renderer.Draw(window, lapsStack.getLatestLap())
	pygame.display.update()
	clock.tick(20)



pygame.quit()
communication.closeSerial()
quit()


