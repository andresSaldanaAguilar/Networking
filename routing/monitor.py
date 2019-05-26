import threading
import os
from ftplib import FTP
import time, datetime
import filecmp

class monitor(threading.Thread):

    def __init__(self,sem,data):
        super(monitor,self).__init__()
        self.sem = sem
        self.data = data
        self.stop = False

    def run(self):
        while not self.stop:

            self.sem.acquire()

            for ip in self.data:
                #creando directorios si no existen
                try:
                    os.mkdir(str(ip))
                except OSError:
                    pass

                #caso cuando ya existen archivos, y comparamos con el archivo mas actual
                if len(os.listdir(os.getcwd()+'/'+ip)) > 0 :

                    latestfile = latestConf(ip)
                    currentfile = time.strftime('%Y-%m-%d')+'-'+time.strftime('%H-%M')

                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    local_filename = os.path.join(r''+os.getcwd()+'/'+ip, currentfile)
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR startup-config', file.write)
                    file.close()
                    ftp.quit()

                    #comparando archivo creado con el archivo con la config mas nueva
                    # true: borramos archivo, no nos interesa
                    # false: lo guardamos y notificamos
                    if filecmp.cmp(os.getcwd()+'/'+ip+'/'+latestfile,os.getcwd()+'/'+ip+'/'+currentfile) :


                #caso cuando es la primera vez y vamos a traer la configuracion inicial
                else:
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    local_filename = os.path.join(r''+os.getcwd()+'/'+ip, time.strftime('%Y-%m-%d')+'-'+time.strftime('%H-%M'))
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR startup-config', file.write)
                    file.close()
                    ftp.quit()

            time.sleep(120)
            self.sem.release()


def latestConf(ip):
    array = os.listdir(os.getcwd()+'/'+ip)
    date = None
    latestdate = None
    for item in array:
        data = item.split('-')
        date2  = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]))
        if date is None:
            date = date2
            latestdate = item
        elif date2 > date:
            date = date2
            latestdate = item
    return latestdate;
