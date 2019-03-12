import sys
import rrdtool
import calendar
import time, threading

class trendGraph(threading.Thread):
    
    def __init__(self,filename,title,umbral = 30):
        super(trendGraph,self).__init__()
        self.filename = filename
        self.title = title
        self.lastLecture = int(rrdtool.last(self.filename+".rrd"))

        self.lastTime = calendar.timegm(time.gmtime())
        #self.lastTime = self.lastLecture
        self.initTime = self.lastTime - 900 #se resta el tiempo en segundos
        self.umbral = umbral

    def run(self):
        while 1:
            ret = rrdtool.graph(self.filename+".png",
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

                    #método de mínimos cuadrados
                     "VDEF:m=carga,LSLSLOPE",
                     "VDEF:b=carga,LSLINT",
                     'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                     "LINE2:tendencia#FFBB00", 
                     


                     #establecer el umbral
                    "CDEF:umbral25=carga,"+str(self.umbral)+",LT,0,carga,IF",
                    "AREA:carga#00FF00:Carga del CPU",
                     "AREA:umbral25#FF9F00:Tráfico de carga mayor que "+str(self.umbral)+"",
                     "HRULE:"+str(self.umbral)+"#FF0000:Umbral 1 - "+str(self.umbral)+"%",
                     

                     #detectar punto de corte
                    'CDEF:cintersect=tendencia,0,EQ,tendencia,0,IF,'+str(self.umbral)+',+,m,/,b,+,100,/,3600,*,'+str(self.initTime)+',+',
                    "VDEF:pintersect=cintersect,MAXIMUM",
                    "COMMENT: Punto",
                    "GPRINT:pintersect:%8.0lf",

                     #detectar cuando se sale del umbral
        )
            



            time.sleep(5)