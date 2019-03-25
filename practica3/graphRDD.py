import sys
import rrdtool
import calendar
import time, threading

class graphRDD(threading.Thread):

    def __init__(self,filename,label1,unit,title,sem):
    	super(graphRDD,self).__init__()
    	self.filename = filename
    	self.label1 = label1
    	self.unit = unit
    	self.title = title
    	self.sem = sem

    def run(self):
        while True:
            self.sem.aquire()
	        endDate = calendar.timegm(time.gmtime()) + 100
        	begDate = calendar.timegm(time.gmtime()) - 100
        	rrdtool.tune(self.filename + ".rrd", '--alpha', '0.05')
        	ret = rrdtool.graph(self.filename+".png",
                    '--start', str(begDate), 
                    '--end', str(endDate), 
                    '--title=' + self.title,
                    "--vertical-label=Bytes/s",
                    '--slope-mode',
                    "DEF:obs=" + self.filename + ".rrd:in:AVERAGE",                    
                    "DEF:pred=" + self.filename + ".rrd:in:HWPREDICT",
                    "DEF:dev=" + self.filename + ".rrd:in:DEVPREDICT",
                    "DEF:fail=" + self.filename + ".rrd:in:FAILURES",

                #"RRA:DEVSEASONAL:1d:0.1:2",
                #"RRA:DEVPREDICT:5d:5",
                #"RRA:FAILURES:1d:7:9:5""
                    "CDEF:scaledobs=obs,8,*",
                    "CDEF:upper=pred,dev,2,*,+",
                    "CDEF:lower=pred,dev,2,*,-",
                    "CDEF:scaledupper=upper,8,*",
                    "CDEF:scaledlower=lower,8,*",
                    "CDEF:scaledpred=pred,8,*",
                "TICK:fail#FDD017:1.0:Fallas",
                "LINE3:scaledobs#00FF00:In traffic",
                "LINE1:scaledpred#FF00FF:Prediccion\\n",
                #"LINE1:outoctets#0000FF:Out traffic",
                "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                "LINE1:scaledlower#0000FF:Lower Bound Average bits in")
            self.sem.release()
            time.sleep(0.25)

        		

