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
		while 1:
		
			if self.label2 is not None:
				ret = rrdtool.graph( self.filename+".png",
				                "--start",str(actualTime),
				                "--vertical-label="+self.unit,
				                "DEF:in="+self.filename+".rrd:in:AVERAGE",
				                "DEF:out="+self.filename+".rrd:out:AVERAGE",
				                "LINE1:in#00FF00:"+self.label1,
				                "LINE1:out#0000FF:"+self.label2)
				               
			else:
				ret = rrdtool.graph( self.filename+".png",
				                "--start",str(actualTime),
				                "--vertical-label="+self.unit,
				                "DEF:in="+self.filename+".rrd:in:AVERAGE",
				                "LINE1:in#0000FF:"+self.label1)

			time.sleep(5)
