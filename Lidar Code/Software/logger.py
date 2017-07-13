

class Logger():
	def __init(self):
		pass

	def Start(self, filename):
		self.file = open(filename, 'w')

	def NewLap(self, frame):
		# frame : Lap object.
		self.file.write(str(int(frame.getTime() * 1000)) + " ") #write timestamp at the beginning of each line in us

		for point in frame.getPointsPolar():
			self.file.write(str(point[1] * 10) + " ") #write measured distance in mm
		for i in range(0, 353 - len(frame.getPointsPolar()) + 1):
			self.file.write('0 ')
		self.file.write('\n')

	def End(self):
		self.file.close()