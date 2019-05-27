import threading
import os
from ftplib import FTP
import time, datetime
import filecmp
from mail import mail

#clase encargada de versionar y notificar cambios en archivo de config
class monitor(threading.Thread):

    def __init__(self,sem,data):
        super(monitor,self).__init__()
        #semaforo para evitar condiciones de carrera
        self.sem = sem
        #ips de los routers
        self.data = data
        #bandera para detener hilo
        self.stop = False

    def run(self):
        while not self.stop:

            self.sem.acquire()

            #checando los archivos de cada router
            for ip in self.data:
                #creando directorios si no existen
                try:
                    os.mkdir(str(ip))
                except OSError:
                    pass

                #caso cuando ya existen archivos, y comparamos con el archivo mas actual
                if len(os.listdir(os.getcwd()+'/'+ip)) > 0 :

                    latestfile = latestConf(ip)
                    currentfile = time.strftime('%Y-%m-%d')+'-'+time.strftime('%H-%M-%S')

                    #creando el nuevo archivo a comparar con el anterior
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    local_filename = os.path.join(r''+os.getcwd()+'/'+ip, currentfile)
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR startup-config', file.write)
                    file.close()
                    ftp.quit()

                    #comparando archivo creado con el archivo con la config mas nueva
                    # true: borramos archivo, no nos interesa
                    if filecmp.cmp(os.getcwd()+'/'+ip+'/'+latestfile,os.getcwd()+'/'+ip+'/'+currentfile) :
                        os.remove(os.getcwd()+'/'+ip+'/'+currentfile)
                    # false: lo conservamos y notificamos
                    else :
                        email = mail('Cambio en confirguración de '+ip,os.getcwd()+'/'+ip+'/'+latestfile,os.getcwd()+'/'+ip+'/'+currentfile,latestfile,currentfile)
                        email.sendMail()
                        print('Cambio de configuración en '+ip+', mail enviado.')

                #caso cuando es la primera vez y vamos a traer la configuracion inicial
                else:
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    local_filename = os.path.join(r''+os.getcwd()+'/'+ip, time.strftime('%Y-%m-%d')+'-'+time.strftime('%H-%M-%S'))
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR startup-config', file.write)
                    file.close()
                    ftp.quit()

            time.sleep(20)
            self.sem.release()

#metodo que consigue el nombre del archivo de config. mas reciente en fecha
def latestConf(ip):
    array = os.listdir(os.getcwd()+'/'+ip)
    date = None
    latestdate = None
    for item in array:
        data = item.split('-')
        date2  = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]))
        #caso base, primer archivo se vuelve el mas reciente
        if date is None:
            date = date2
            latestdate = item
        #comparamos fechas, si es mayor el archivo conseguido, se vuelve el mas reciente
        elif date2 > date:
            date = date2
            latestdate = item
    return latestdate;
