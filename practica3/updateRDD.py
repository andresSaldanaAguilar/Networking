import time
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

class updateRDD():

	def __init__(self,filename,community,host,oid1,port):
		super(updateRDD,self).__init__()
		self.filename = filename
		self.community = community
		self.host = host
		self.oid1 = oid1
		self.port = port
	
	def update(self):
		total_input_traffic = requestRT(self.community,self.host,self.oid1,self.port)
			

		#checando si hay respuesta
		if (total_input_traffic != ""):
			valor = "N:" + str(total_input_traffic)
			rrdtool.update(self.filename+'.rrd', valor)
			rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
		#else:
			#no hay respuesta
			#print("sin respuesta del agente: "+self.host)

				
		

