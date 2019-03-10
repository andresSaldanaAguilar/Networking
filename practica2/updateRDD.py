import time, threading
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

class updateRDD(threading.Thread):

	def __init__(self,filename,community,host,oid1,oid2,port):
		super(updateRDD,self).__init__()
		self.filename = filename
		self.community = community
		self.host = host
		self.oid1 = oid1
		self.oid2 = oid2
		self.port = port
	
	def run(self):
		while 1:
			total_input_traffic = requestRT(self.community,self.host,self.oid1,self.port)
				
			if self.oid2 is not None:
				total_output_traffic = requestRT(self.community,self.host,self.oid2,self.port)
				#checando si hay respuesta
				if (total_input_traffic != "" and total_output_traffic != ""):
					valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
					#print("valor de oid: "+valor)
					rrdtool.update(self.filename+'.rrd', valor)
					rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
				#else:
					#no hay respuesta
					#print("sin respuesta del agente: "+self.host)
				time.sleep(5)
			
			else:
				#checando si hay respuesta
				if (total_input_traffic != ""):
					valor = "N:" + str(total_input_traffic)
					rrdtool.update(self.filename+'.rrd', valor)
					rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
				#else:
					#no hay respuesta
					#print("sin respuesta del agente: "+self.host)
				time.sleep(5)
				
		

		#if ret:
			#print (rrdtool.error())
			#time.sleep(10)
