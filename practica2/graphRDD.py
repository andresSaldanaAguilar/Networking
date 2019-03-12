import sys
import rrdtool
import calendar
import time, threading


class graphRDD(threading.Thread):
	
	def __init__(self,filename,label1,label2,unit,title):
		super(graphRDD,self).__init__()
		self.filename = filename
		self.label1 = label1
		self.label2 = label2
		self.unit = unit
		self.title = title
			
	def run(self):
		actualTime = calendar.timegm(time.gmtime())
		while 1:
		
			if self.label2 is not None and self.label2 != "On use":
				ret = rrdtool.graph( self.filename+".png",
				                "--start",str(actualTime),
				                "--title="+self.title,
				                "--vertical-label="+self.unit,
				                "DEF:in="+self.filename+".rrd:in:AVERAGE",
				                "DEF:out="+self.filename+".rrd:out:AVERAGE",
				                "LINE1:in#00FF00:"+self.label1,
				                "LINE1:out#0000FF:"+self.label2
				                )
				                
			elif self.label2 == "On use":
				ret = rrdtool.graph( self.filename+".png",
				                "--start",str(actualTime),
				                "--title="+self.title,
				                "--vertical-label="+self.unit,
				                "DEF:tin="+self.filename+".rrd:tin:AVERAGE",
				                "DEF:tout="+self.filename+".rrd:tout:AVERAGE",
				                "DEF:pin="+self.filename+".rrd:pin:AVERAGE",
				                "DEF:pout="+self.filename+".rrd:pout:AVERAGE",
				                "CDEF:tmul=tin,tout,*",
				                "CDEF:pmul=pin,pout,*",
				                "LINE1:tmul#0000FF:"+self.label1,
				                "LINE1:pmul#FF0000:"+self.label2
				                )
				                				               
			else:
				ret = rrdtool.graph( self.filename+".png",
				                "--start",str(actualTime),
				                "--title="+self.title,
				                "--vertical-label="+self.unit,
				                "DEF:in="+self.filename+".rrd:in:AVERAGE",
				                "LINE1:in#0000FF:"+self.label1)

			time.sleep(5)
			
			
				                #"CDEF:min=in,out,MAX",
				                #"CDEF:max=in,out,GT,in,out,IF",
				                #"LINE1:sum#FF0000:sum",
				                #"LINE1:min#FF00FF:min",
