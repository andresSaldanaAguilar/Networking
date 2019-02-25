import time, threading
import rrdtool
from getSNMP import *
total_input_traffic = 0
total_output_traffic = 0

class updateRDD(threading.Thread):

	def __init__(self,filename,community,host,oid1,oid2):
		super(updateRDD,self).__init__()
		self.filename = filename
		self.community = community
		self.host = host
        self.oid1 = oid1
        self.oid2 = oid2
	
	def run(self):
		while 1:
		    total_input_traffic = int(
		        requestRT(self.community,self.host,self.oid1))
		    total_output_traffic = int(
		        requestRT(self.community,self.host,self.oid2))

		    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
		    rrdtool.update(self.filename+'.rrd', valor)
		    rrdtool.dump(self.filename+'.rrd',self.filename+'.xml')
		    time.sleep(5)

		if ret:
		    print (rrdtool.error())
		    time.sleep(10)
