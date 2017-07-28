from diy_lidar import DIYLidar
from breezyslam.algorithms import RMHC_SLAM
from pltslamshow import SlamShow

class DIYLidar_Properties(object):
    '''
    A class representing the specifications of a scanning laser rangefinder (Lidar).
    '''
    def __init__(self, points_per_lap, detection_margin=0, offset_mm=0):
    	print "PPL = " + str(points_per_lap)
        self.scan_size = points_per_lap
        self.scan_rate_hz = 1.57
        self.detection_angle_degrees = 360
        self.distance_no_detection_mm = 10000 #10m
        self.detection_margin = 0
        self.offset_mm = offset_mm

WINDOW_SIZE = 1200
MAP_SIZE_METERS = 10

lidar = DIYLidar(log = False)
lidar_properties = DIYLidar_Properties(lidar.getPointsPerLap())

mapbytes = bytearray(WINDOW_SIZE * WINDOW_SIZE)
slam = RMHC_SLAM(lidar_properties, WINDOW_SIZE, 35) 

window = SlamShow(WINDOW_SIZE, MAP_SIZE_METERS*1000/WINDOW_SIZE, "scan")
pose = [0,0,0]

while True:
	scan = lidar.waitForNextScan()
	if scan != False:
		slam.update(scan.getPointsDistances_mm())
		x, y, theta = slam.getpos()
		pose = [x /10.0, y / 10.0, theta]
		slam.getmap(mapbytes)


		window.displayMap(mapbytes)
		window.setPose(*pose)

		if not window.refresh():
			lidar.Quit()
			exit(0)