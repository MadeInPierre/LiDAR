import serial.tools.list_ports
from serial_manager import *
from logger import *


class DIYLidar():
	def __init__(self, log = False):
		self.logger = Logger()
		if log:
			self.logger.Start("log.dat")


		# Find the lidar in the conneced USB devices and open serial connection.
		connection_port = ""
		available_ports = list(serial.tools.list_ports.comports())
		for p in available_ports:
			if "Serial" in str(p):
				connection_port = str(p).split(' ')[0]
				break
		self.communication = SerialManager(connection_port, 500000)
		self.communication.openSerial()

		# Get the angular resolution from the lidar
		PointsPerLap = self.communication.getPointsPerLap() + 1
		self.lapsStack = LapsStack(PointsPerLap)

		# initiate lidar and start scanning
		self.communication.resetLidar()
		self.communication.setSpeed(3, self.lapsStack)


	def waitForNextScan(self):
		# The function waits until a lap is sent and parses the result.
		self.communication.updateSerial(lapsStack = self.lapsStack, logger = self.logger)
		if self.lapsStack.isNewLap():
			return self.lapsStack.getLastLap()
		else:
			return False

	def getPointsPerLap(self):
		return self.lapsStack.getPointsPerLap()

	def Quit(self):
		self.communication.setSpeed(0, self.lapsStack)
		self.communication.closeSerial()
		self.logger.End()