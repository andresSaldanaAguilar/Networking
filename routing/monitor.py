import threading
import os

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
            self.sem.release()
