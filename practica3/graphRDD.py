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
        self.penultima_falla = None


    def run(self):
        while True:
            self.sem.acquire()
            endDate = rrdtool.last(self.filename + ".rrd")
            begDate = endDate - 2000  
            #rrdtool.tune(self.filename + ".rrd", '--alpha', '0.99')
            ret = rrdtool.graphv(
                    self.filename+".png",
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
                "LINE1:scaledupper#ff0000:Upper Bound Average bits in\\n",
                "LINE1:scaledlower#0000FF:Lower Bound Average bits in",

                "VDEF:lastfail=fail,LAST",
                "PRINT:lastfail: %c :strftime",
                "PRINT:lastfail:%6.2lf %S ",
                'PRINT:fail:MIN:%1.0lf',
                'PRINT:fail:MAX:%1.0lf'
                )


            if("nan" not in ret['print[1]']):
                time_falla=ret['print[0]']
                ultima_falla= int(float(ret['print[1]'].strip()))
                fmin= int(ret['print[2]'])
                fmax= int(ret['print[3]'])
                print(time_falla + "-" + str(ultima_falla) + "-" + str(self.penultima_falla)+" "+self.filename)


                #siguientes detecciones
                if(self.penultima_falla != None):
                    if(self.penultima_falla != ultima_falla):
                        if(ultima_falla == 1):
                            print("deteccion de error en" + self.filename + "a las "+time_falla)
                            self.penultima_falla = ultima_falla
                        elif(ultima_falla == 0):
                            print("fin de falla en" + self.filename + "a las "+time_falla)
                            self.penultima_falla = ultima_falla
                    else:
                        print("sin falla en "+ self.filename)

                #primeras detecciones
                elif(fmin != fmax):
                    if(ultima_falla == 1):
                        print("deteccion de error en" + self.filename + "a las "+time_falla)
                        self.penultima_falla = ultima_falla
                    elif(ultima_falla == 0):
                        print("fin de error en" + self.filename + "a las "+time_falla)
                        self.penultima_falla = ultima_falla

                else:
                    print("sin falla en "+ self.filename)

            else:
                time_falla=ret['print[0]']
                ultima_falla= ret['print[1]']
                fmin= ret['print[2]']
                fmax= ret['print[3]']
                print(time_falla + "-" + ultima_falla + "-" + fmin + "-" + fmax+"-"+self.filename)            

            self.sem.release()
            time.sleep(0.25)

                

  
