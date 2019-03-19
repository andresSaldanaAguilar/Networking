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
		self._stop_event = True
			
	def run(self):
		actualTime = calendar.timegm(time.gmtime())
		while self.stopped():
		
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
							
			#caso especial para RAM y PROCESAMIENTO  
			elif self.label2 == "On use":
				ret = rrdtool.graph( self.filename+".png",
								"--start",str(actualTime),
								"--title="+self.title,
								"--vertical-label="+self.unit,
								#definiendo los limites
								'--lower-limit', '0',
								'--upper-limit', '100',
								#haciendo el calculo del total del recurso y el recurso usado
								"DEF:tin="+self.filename+".rrd:tin:AVERAGE",
								"DEF:tout="+self.filename+".rrd:tout:AVERAGE",
								"DEF:pin="+self.filename+".rrd:pin:AVERAGE",
								"DEF:pout="+self.filename+".rrd:pout:AVERAGE",
								#calculando el porcentaje usado
								"CDEF:tmul=tin,tout,*",
								"CDEF:pmul=pin,pout,*",
								"CDEF:pused=pmul,100,*", 
								"CDEF:tused=pused,tmul,/",    
								"LINE1:tused#FF0000:"+self.label2
								)
					
			#aqui manejamos el caso de los cores, pero este valor ya viene en porcentaje, asi que no hay que calcular nada          				               
			else:
				ret = rrdtool.graph( self.filename+".png",
								"--start",str(actualTime),
								"--title="+self.title,
								"--vertical-label="+self.unit,
								"DEF:in="+self.filename+".rrd:in:AVERAGE",
								"LINE1:in#0000FF:"+self.label1)

			time.sleep(5)
			
			
	def stop(self):
		self._stop_event = False

	def stopped(self):
		return self._stop_event
