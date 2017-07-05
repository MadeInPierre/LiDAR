import serial, time

class LapsStack():
	def __init__(self):
		pass


class Lap():
	def __init__(self, points_per_lap, lap_count):
		self.POINTS_PER_LAP = points_per_lap
		self.LapCount = lap_count
		self.PointsDistances = [] #1D array with only distance values per measurement.

		self.PointsFinal = [] #once PointsDistance is full, self.analyse() guesses the angles based on POINTS_PER_LAP and the array length.

		self.StartTime = time.time() * 1000
		self.EndTime = 0

		self.LapEnded = False

	def AddPoint(self, distance):
		self.PointsDistances.append(distance)

	def EndLap(self):
		self.LapEnded = True
		self.EndTime = time.time() * 1000
		self.analyse()

	def GetPoints(self):
		if self.LapEnded:
			return self.PointsFinal
		else:
			return False #TODO better error check ? 

	def analyse(self):
		if tickError() == 0:
			angle_increment = 360 / len(self.PointsDistances) # angle in degrees
			for i in range(0, len(self.PointsDistances)):
				self.PointsFinal = (i * angle_increment, self.PointsDistances[i])

		else:
			print(str(tickError()) + " receive error.")

	def receiveError(self):
		# When scanning starts, the lidar sends the number of ticks expected per lap.
		# This functions compares this number with the number of measurements received.
		# Since we should get one measurement per tick, these two numbers are compared to get the amount of data loss.
		# (just a debug function)
		print("PPL = " + str(self.POINTS_PER_LAP) + ", got " + str(len(self.PointsDistances)) + " points.") #VERBOSE
		return len(self.PointsDistances) - self.POINTS_PER_LAP



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