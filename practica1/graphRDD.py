import sys
import rrdtool
import calendar
import time

def graphRDD(filename):
    actualTime = calendar.timegm(time.gmtime())
    while 1:
        ret = rrdtool.graph( filename+".png",
                        "--start",str(actualTime),
                        "--vertical-label=Bytes/s",
                        "DEF:inoctets"+filename+"=.rrd:inoctets:AVERAGE",
                        "DEF:outoctets"+filename+"=.rrd:outoctets:AVERAGE",
                        "AREA:inoctets#00FF00:In traffic",
                        "LINE1:outoctets#0000FF:Out traffic\r")

        time.sleep(30)