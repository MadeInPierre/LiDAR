import serial, time


class SerialManager():
	def __init__(self, PORT, SPEED):
		self.SERIAL = serial.Serial()
		self.SERIAL.baudrate = SPEED
		self.SERIAL.port = PORT
		self.SERIAL.timeout = 2

		self.last_points_time = time.time() * 1000

	def getSerialInput(self):
		if self.SERIAL.is_open:
			if self.SERIAL.inWaiting():
				data = self.SERIAL.readline()
				#print(data + "\n\n\n\n")

				array = self.dataToLidarArray(data)
				return array
			else:
				return None
		else:
			return None

	def dataToLidarArray(self, data):
		if data[0].isdigit():
			result = []


			points = data.split(',')
			for point in points :
				if "-" in point:
					degree, distance = point.split('-')
					result.append((float(degree), int(distance)))

			self.incertitude(result)


			hz = 1000 / (time.time() * 1000 - self.last_points_time)
			print "Hz = " + str(hz)
			self.last_points_time = time.time() * 1000
			return result
		else:
			print(data)
			return None


	def openSerial(self):
		self.SERIAL.open()
	def closeSerial(self):
		self.SERIAL.close()


	def incertitude(self, points):
		maxx = 0
		minn = 40000
		for p in points:
			if p[1] != 1:
				if p[1] > maxx:
					maxx = p[1]
				if p[1] < minn:
					minn = p[1]
		print(maxx - minn)