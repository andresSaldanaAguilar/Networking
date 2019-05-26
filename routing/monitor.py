import threading
import os
from ftplib import FTP
import time

class monitor(threading.Thread):

    def __init__(self,sem,data):
        super(monitor,self).__init__()
        self.sem = sem
        self.data = data
        self.stop = False

    def run(self):
        while not self.stop:
            self.sem.acquire()

            #creando directorios si no existen
            for ip in self.data:
                try:
                    os.mkdir(str(ip))
                except OSError:
                    pass
                else:
                    pass

                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                local_filename = os.path.join(r''+os.getcwd()+'/'+ip, time.strftime("%d-%m-%Y")+"_"+time.strftime("%H:%M"))
                file = open(local_filename, 'wb')
                ftp.retrbinary('RETR startup-config', file.write)
                file.close()
                ftp.quit()

            time.sleep(60)
            self.sem.release()
