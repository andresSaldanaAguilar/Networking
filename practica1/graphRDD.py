import sys
import rrdtool
import calendar
import time, threading


class graphRDD(threading.Thread):
	
	def __init__(self,filename):
		super(graphRDD,self).__init__()
		self.filename = filename
			
	def run(self):
		actualTime = calendar.timegm(time.gmtime())
		print(self.filename)
		while 1:
		    ret = rrdtool.graph( self.filename+".png",
		                    "--start",str(actualTime),
		                    "--vertical-label=Bytes/s",
		                    "DEF:inoctets="+self.filename+".rrd:inoctets:AVERAGE",
		                    "DEF:outoctets="+self.filename+".rrd:outoctets:AVERAGE",
		                    "AREA:inoctets#00FF00:In traffic",
		                    "LINE1:outoctets#0000FF:Out traffic\r")

		    time.sleep(5)
