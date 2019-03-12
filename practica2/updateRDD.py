import time, threading
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

class updateRDD(threading.Thread):

	def __init__(self,filename,community,host,oid1,oid2,oid3,oid4,port):
		super(updateRDD,self).__init__()
		self.filename = filename
		self.community = community
		self.host = host
		self.oid1 = oid1
		self.oid2 = oid2
		self.oid3 = oid3
		self.oid4 = oid4		
		self.port = port
	
	def run(self):
		while 1:
			total_input_traffic = requestRT(self.community,self.host,self.oid1,self.port)
				
			if self.oid2 is not None and self.oid3 is None and self.oid4 is None:
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
				
			elif self.oid2 is not None and self.oid3 is not None and self.oid4 is not None:
				total_output_traffic = requestRT(self.community,self.host,self.oid2,self.port)
				partial_input_traffic = requestRT(self.community,self.host,self.oid4,self.port)
				partial_output_traffic = requestRT(self.community,self.host,self.oid3,self.port)
				#checando si hay respuesta
				if (total_input_traffic != "" and total_output_traffic != "" and partial_output_traffic != "" and partial_input_traffic != ""):
					valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic) + ':' + str(partial_input_traffic) + ':' + str(partial_output_traffic)
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
					#print("valor de oid: "+valor)
					rrdtool.update(self.filename+'.rrd', valor)
					rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
				#else:
					#no hay respuesta
					#print("sin respuesta del agente: "+self.host)
				time.sleep(5)
				
		

		#if ret:
			#print (rrdtool.error())
			#time.sleep(10)
