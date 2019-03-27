#!/usr/bin/env pythongns
import os
import threading
import time
import rrdtool
import tempfile
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class errorMonitor(threading.Thread):

  def __init__(self,filename,sem):
    super(errorMonitor,self).__init__()
    self.filename = filename
    self.sem = sem 

  def run(self):
    time.sleep(10)
    while True:
      self.sem.acquire()
      status = self.check_aberration(self.filename)
      if status == 1:
        print("inicio de error en "+self.filename)
      elif status == 2:
        print("fin de error en "+self.filename)
      self.sem.release()


  def check_aberration(self,filename):
      """ This will check for begin and end of aberration
          in file. Will return:
          0 if aberration not found.
          1 if aberration begins
          2 if aberration ends
      """
      ab_status = 0
      rrdfilename = filename+".rrd"

      info = rrdtool.info(rrdfilename)
      rrdstep = int(info['step'])
      lastupdate = info['last_update']
      previousupdate = str(lastupdate - rrdstep )
      graphtmpfile = tempfile.NamedTemporaryFile()
      # Ready to get FAILURES  from rrdfile
      # will process failures array values for time of 2 last updates
      values = rrdtool.graph(graphtmpfile.name+'F',
                             'DEF:f0=' + rrdfilename + ':in:FAILURES:start=' + previousupdate + ':end=' + str(lastupdate),
                             'PRINT:f0:MIN:%1.0lf',
                             'PRINT:f0:MAX:%1.0lf',
                             'PRINT:f0:LAST:%1.0lf')
      print (values)
      try: 
        fmin = int(values[2][0])
        fmax = int(values[2][1])
        flast = int(values[2][2])
        print ("fmin="+fmin+", fmax="+fmax+",flast="+flast)
        # check if failure value had changed.
        if (fmin != fmax):
            if (flast == 1):
                ab_status = 1
            else:
                ab_status = 2
        return ab_status
      except:
        return

