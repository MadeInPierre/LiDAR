import pygame
from renderer import Renderer
from serial_manager import *
from analyser import *

'''
TODO/FEATURELIST:
	- New keyboard keys
		- S, F, U for Slow, Fast and Ultra mode. Hotswap the mode while running
		- O for resetting the 0 angle position (Offset)
'''


pygame.init()
clock = pygame.time.Clock()

WindowRes = (1600, 1600)
window = pygame.display.set_mode(WindowRes)
pygame.display.set_caption("LIDAR Cloud POV")

renderer = Renderer(WindowRes)
try:
	communication = SerialManager("/dev/ttyUSB0", 500000)
except:
	communication = SerialManager("/dev/ttyUSB1", 500000)

communication.openSerial()

PointsPerLap = communication.getPointsPerLap()
print("Got PPL = " + str(PointsPerLap))
lapsStack = LapsStack(PointsPerLap)

communication.resetLidar()
communication.setSpeed(2, lapsStack)


analyser = Analyser()

running = True
while running:
	events = pygame.event.get()
	for event in events: # quitting the program
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			running = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
			renderer.Zoom()
		if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
			renderer.UnZoom()
		if event.type == pygame.KEYDOWN and event.key == 224: # azerty key 0
			communication.setSpeed(0, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == 38:  # azerty key 1
			communication.setSpeed(1, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == 233: # azerty key 2
			communication.setSpeed(2, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == 34:  # azerty key 3
			communication.setSpeed(3, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == 39:  # azerty key 4
			communication.setSpeed(4, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == 40:  # azerty key 5
			communication.setSpeed(5, lapsStack)
		if event.type == pygame.KEYDOWN and event.key == pygame.K_r:  # azerty key 5
			communication.resetLidar()





	serial_update = communication.updateSerial(lapsStack = lapsStack)

	if lapsStack.getNumberOfLaps() > 0:
		renderer.Draw(window, lapsStack, analyser)
	pygame.display.update()
	clock.tick(20)


communication.setSpeed(0, lapsStack)
pygame.quit()
communication.closeSerial()
quit()


