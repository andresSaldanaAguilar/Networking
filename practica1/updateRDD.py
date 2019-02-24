import time
import rrdtool
from getSNMP import request
total_input_traffic = 0
total_output_traffic = 0

def updateRDD(filename,community,host,oid1,oid2):
    while 1:
        total_input_traffic = int(
            request(community,host,oid1))
        total_output_traffic = int(
            request(community,host,oid2))

        valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
        print (valor)
        rrdtool.update(filename+'.rrd', valor)
        rrdtool.dump(filename+'.rrd',filename+'.xml')
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)
