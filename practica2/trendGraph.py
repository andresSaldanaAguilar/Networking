import sys
import rrdtool
import calendar
import time, threading
from umbrales import *

class trendGraph(threading.Thread):
    
    def __init__(self,filename,title,umbral1 = 20,umbral2 = 80,umbral3 = 90):
        super(trendGraph,self).__init__()
        self.filename = filename
        self.title = title
        self.lastLecture = int(rrdtool.last(self.filename+".rrd"))

        self.lastTime = calendar.timegm(time.gmtime())
        #self.lastTime = self.lastLecture
        self.initTime = self.lastTime - 900 #se resta el tiempo en segundos
        self.umbral1 = umbral1
        self.umbral2 = umbral2
        self.umbral3 = umbral3

    def run(self):
        while 1:
            ret = rrdtool.graphv(self.filename+".png",
                     "--start",str(self.initTime),
                     "--end",str(self.lastTime+900),
                     "--vertical-label=Carga CPU",
                     "--title=Uso de CPU "+str(self.title),
                     "--color", "ARROW#009900",
                     '--vertical-label', "Uso de CPU (%)",
                     '--lower-limit', '0',
                     '--upper-limit', '100',

                     "DEF:carga="+self.filename+".rrd:CPUload:AVERAGE",
                     "AREA:carga#00FF00:Carga CPU",
                     "LINE1:30",
                     "AREA:5#ff000022:stack",
                     
                     #datos del CPU
                     "VDEF:CPUlast=carga,LAST",
                     "VDEF:CPUmin=carga,MINIMUM",
                     "VDEF:CPUavg=carga,AVERAGE",
                     "VDEF:CPUmax=carga,MAXIMUM",
                     "VDEF:cargaSTDEV=carga,STDEV",
                     "VDEF:cargaLAST=carga,LAST",
                     

                    #grafica de los datos del CPU
                    "COMMENT:Now          Min             Avg             Max",
                     "GPRINT:CPUlast:%12.0lf%s",
                     "GPRINT:CPUmin:%10.0lf%s",
                     "GPRINT:CPUavg:%13.0lf%s",
                     "GPRINT:CPUmax:%13.0lf%s",
                     "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                     "GPRINT:cargaLAST:%6.2lf %SLAST",
                    "PRINT:CPUmax:%6.2lf %S",

                    #método de mínimos cuadrados
                     "VDEF:m=carga,LSLSLOPE",
                     "VDEF:b=carga,LSLINT",
                     'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                     "LINE2:tendencia#FFBB00", 
                     "CDEF:abc2=tendencia,90,100,LIMIT",
                     "VDEF:minabc2=abc2,FIRST",


                     #establecer el umbral1
                    "CDEF:umbral25=carga,"+str(self.umbral1)+",LT,0,carga,IF",
                    "AREA:carga#00FF00:Carga del CPU",
                    "AREA:umbral25#FF9F00:Tráfico de carga mayor que "+str(self.umbral1)+"",
                    "HRULE:"+str(self.umbral1)+"#0EBC28:Umbral 1 - "+str(self.umbral1)+"%",

                    #establecer el umbral 2
                     "CDEF:umbral30=carga,"+str(self.umbral2)+",LT,0,carga,IF",
                    "AREA:carga#00FF00:Carga del CPU",
                     "AREA:umbral30#FF9F00:Tráfico de carga mayor que "+str(self.umbral2)+"",
                     "HRULE:"+str(self.umbral2)+"#E1D71E:Umbral 2 - "+str(self.umbral2)+"%",

                    #establecer el umbral 3
                     "CDEF:umbral35=carga,"+str(self.umbral3)+",LT,0,carga,IF",
                    "AREA:carga#00FF00:Carga del CPU",
                     "AREA:umbral35#FF9F00:Tráfico de carga mayor que "+str(self.umbral3)+"",
                     "HRULE:"+str(self.umbral3)+"#FF0000:Umbral 3 - "+str(self.umbral3)+"%",
                     
                     

                     #detectar punto de corte
                    'CDEF:cintersect=tendencia,0,EQ,tendencia,0,IF,'+str(self.umbral1)+',+,m,/,b,+,100,/,900,*,'+str(self.initTime)+',+',
                    "VDEF:pintersect=cintersect,MAXIMUM",
                    "COMMENT: Punto",
                    #"GPRINT:pintersect:%c:strftime"

                     #detectar cuando se sale del umbral
                     "PRINT:minabc2: %c:strftime"
        )
            
            lastValue = ret['print[0]']
            fechaBien = ret['print[1]']
            print("Fecha bien"+fechaBien)
            if checkErrors(lastValue,self.umbral1):
                print("manda mail")
                #sendEmail(self.filename,"CPU")

            print("ultimo valor max: "+lastValue)


            time.sleep(5)