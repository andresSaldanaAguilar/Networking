import rrdtool

def createRDD(filename):   
    ret = rrdtool.create(filename+".rrd",
                        "--start",'N',
                        "--step",'5',
                        "DS:inoctets:COUNTER:600:U:U",
                        "DS:outoctets:COUNTER:600:U:U",
                        "RRA:AVERAGE:0.5:6:600",
                        "RRA:AVERAGE:0.5:1:600")
    if ret:
        print (rrdtool.error())


