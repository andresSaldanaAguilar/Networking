import sys
import rrdtool
import calendar
import time, threading


class graphRDD(threading.Thread):
	
	def __init__(self,filename,label1,label2,unit):
		super(graphRDD,self).__init__()
		self.filename = filename
		self.label1 = label1
		self.label2 = label2
		self.unit = unit
			
	def run(self):
		actualTime = calendar.timegm(time.gmtime())
		print(self.filename)
		while 1:
		    ret = rrdtool.graph( self.filename+".png",
		                    "--start",str(actualTime),
		                    "--vertical-label="+unit,
		                    "DEF:in="+self.filename+".rrd:in:AVERAGE",
		                    "DEF:out="+self.filename+".rrd:out:AVERAGE",
		                    "AREA:in#00FF00:"+label1,
		                    "LINE1:out#0000FF:"+label2)

		    time.sleep(5)
