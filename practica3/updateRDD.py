import time, threading
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

class updateRDD(threading.Thread):

	def __init__(self,filename,community,host,oid1,port,sem):
		super(updateRDD,self).__init__()
		self.filename = filename
		self.community = community
		self.host = host
		self.oid1 = oid1
		self.port = port
		self.sem = sem 
	
	def run(self):
		while True:
			self.sem.acquire()
			total_input_traffic = requestRT(self.community,self.host,self.oid1,self.port)
			#checando si hay respuesta
			if (total_input_traffic != ""):
				valor = "N:" + str(total_input_traffic)
				rrdtool.update(self.filename+'.rrd', valor)
				rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
			#else:
				#no hay respuesta
				#print("sin respuesta del agente: "+self.host)
			self.sem.release()
			time.sleep(0.25)

				
		

