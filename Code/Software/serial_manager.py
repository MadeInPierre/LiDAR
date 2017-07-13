import serial, time, math

class SerialParser():
	def __init__(self):
		pass

	def Parse(self, data, lapsStack):
		# If data is valid, returns a Lap object.

		###### PROTOCOL STRUCTURE FOR A LAP : L12(-176):dist1,dist2,...,dist176,\r\n
		###### 12 = Lap number, "-176" only on lap 0 - gives the number of tiks per lap.

		if len(data) < 3:
			pass # empty message, used for synchronisation. Ignore it.
		elif "RESET" in data:
			return True #confirm that reset occured
		elif 'P' in data and data[-1] == '\n':
			# The Lidar just gave the angular resolution (PointsPerLap) in format 'P176\n'.
			return int(data[data.index('P') + 1:])
		elif data[0] == 'L' and data[-1] == '\n':
			# If the start and end of the message is correct for a full lap data, we assume this is correct and create a new lap object with it.

			# Analyse header (format ! 'L12:' or 'L0-177:')
			data_header, data_points = data.split(':')
			lap_count = int(data_header[1:])

			print "Lap " + str(lap_count),

			points = map(int, data_points.split(',')[:-1])

			#print("Points = " + str(points)) #VERBOSE
			print("(" + str(len(points)) + " points)")


			# Create a lap with this data
			if abs(self.receiveError(lapsStack.getPointsPerLap(), points)) < lapsStack.getPointsPerLap() * 0.5: # discard the scan if there are too much or less points compared to the reference/resolution
				lapsStack.NewLap(Lap(lap_count, points, points_per_lap = lapsStack.getPointsPerLap()))
			else:
				print("[WARNING] Too many or too less points, discarted the lap.")
		elif data[0] == 'L' and data[-1] != '\n':
			print("[WARNING] Received non full-lap message from lidar")
		else:
			print("[NOT_RECOGNIZED] >>> " + data)
			return False


	def receiveError(self, points_per_lap, points):
		# When scanning starts, the lidar sends the number of ticks expected per lap at Lap0.
		# This functions compares this number with the number of measurements received.
		# Since we should get one measurement per tick, these two numbers are compared to get the amount of data loss.
		# (just a debug function)
		#print("PPL = " + str(self.POINTS_PER_LAP) + ", got " + str(len(self.PointsDistances)) + " points.") #VERBOSE
		error = len(points) - points_per_lap
		if error != 0:
			pass#print("[WARNING] The lap does not have the right number of points (error = " + str(error) + ". Using the number of points for calculus of angle.")
		return error






class LapsStack():
	def __init__(self, points_per_lap):
		self.Stack = []
		self.PointsPerLap = points_per_lap
		self.CurrentLidarSpeed = 0

	def NewLap(self, lap):
		lap.LidarSpeed = self.CurrentLidarSpeed
		self.Stack.append(lap)

	def ResetStack(self):
		self.Stack = []

	def setPointsPerLap(self, PPL):
		self.PointsPerLap = PPL
	def getPointsPerLap(self):
		return self.PointsPerLap

	def getNumberOfLaps(self):
		return len(self.Stack)
	def getLastLap(self):
		if len(self.Stack) > 0:
			return self.Stack[-1]
		return None

	def getLastHz(self):
		if len(self.Stack) >= 2:
			return 1 / ((self.Stack[-1].ReceivedTime - self.Stack[-2].ReceivedTime) * 0.001)
		else:
			return 0





class Lap():
	def __init__(self, lap_count, points, points_per_lap = -1):
		self.LapCount = lap_count
		self.LidarSpeed = 0
		self.POINTS_PER_LAP = points_per_lap
		self.PointsDistances = points
		self.ReceivedTime = time.time() * 1000

		self.PointsFinal = []

		self.filterNoise()
		self.findAngles()

	def findAngles(self):
		angle_increment = 360 / float(self.POINTS_PER_LAP) # angle in degrees
		i = 0
		for point in self.PointsDistances:
			self.PointsFinal.append((i * angle_increment, self.PointsDistances[i]))
			i += 1

	def filterNoise(self):
		#remove points with distance = 1 (1 is given from the lidar when the distance was not found)
		done = False
		i = 0
		for point in self.PointsDistances:
			if point == 1:
				point = 0
		'''
		while done == False:
			if i < len(self.PointsFinal):
				if self.PointsFinal[i][1] == 1:
					del self.PointsFinal[i]
					i = 0
			else:
				done = True
		'''



	def setPointsPerLap(self, PPL):
		self.POINTS_PER_LAP = PPL

	def getPointsPolar(self):
		return self.PointsFinal
	def getPointsCartesian(self):
		points_cart = []
		for p in self.PointsFinal:
			a = math.radians(p[0])
			position = (p[1] * math.cos(a), p[1] * math.sin(a))
			points_cart.append(position)
		return points_cart



class SerialManager():
	def __init__(self, PORT, SPEED):
		self.SERIAL = serial.Serial()
		self.SERIAL.baudrate = SPEED
		self.SERIAL.port = PORT
		self.SERIAL.timeout = 1.5

		self.last_points_time = time.time() * 1000

		self.serialParser = SerialParser()

	def updateSerial(self, lapsStack = None, waitForResponse = False):
		if self.SERIAL.is_open:
			if self.SERIAL.inWaiting() or waitForResponse == True:
				data = self.SERIAL.readline() # returns a string until \n
				#print("\n\n\nRAW : " + data)  # VERBOSE
				parse_response = self.serialParser.Parse(data, lapsStack) # Parse the output and create Laps with it.
				return parse_response
			else:
				return False
		else:
			return None

	def resetLidar(self):
		self.SERIAL.write('R')
		response = self.updateSerial(waitForResponse = True)
		if response == False:
			print("[ERROR] RESET NOT CORRECT")
		else:
			print("[OK] Reset correct")

	def getPointsPerLap(self):
		self.SERIAL.write('P')
		return self.updateSerial(waitForResponse = True)

	def setSpeed(self, speed, lap_stack):
		print "[INFO] Setting Lidar speed " + str(speed)
		self.SERIAL.write(str(speed))
		lap_stack.CurrentLidarSpeed = speed
				

	def openSerial(self):
		self.SERIAL.open()
	def closeSerial(self):
		self.SERIAL.close()

	def bytes_to_int(self, bytes_array): # gets an array of bytes and gives a int by joining these bytes.
		joined_bytes = b''.join(buf)
		return int(joined_bytes)





