import rrdtool

def createRDD(filename,numcol): 
	if numcol == 1:
		ret = rrdtool.create(filename+".rrd",
		                    "--start",'N',
		                    "--step",'10',
		                    "DS:in:COUNTER:60:U:U",
		                    "RRA:AVERAGE:0.5:6:600",
		                    "RRA:AVERAGE:0.5:1:600")  
	else:
		ret = rrdtool.create(filename+".rrd",
		                    "--start",'N',
		                    "--step",'10',
		                    "DS:in:COUNTER:60:U:U",
		                    "DS:out:COUNTER:60:U:U",
		                    "RRA:AVERAGE:0.5:6:600",
		                    "RRA:AVERAGE:0.5:1:600")
    if ret:
        print (rrdtool.error())


