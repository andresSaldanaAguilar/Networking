import rrdtool

def createRDD(filename):   
    ret = rrdtool.create(filename+".rrd",
                        "--start",'N',
                        "--step",'10',
                        "DS:inoctets:COUNTER:60:U:U",
                        "DS:outoctets:COUNTER:60:U:U",
                        "RRA:AVERAGE:0.5:6:600",
                        "RRA:AVERAGE:0.5:1:600")
    if ret:
        print (rrdtool.error())


