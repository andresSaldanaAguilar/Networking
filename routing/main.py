import os
from ftplib import FTP
import json
from monitor import monitor
import threading

class RouterManager():

    def __init__(self):
        self.data = {}
        #base de datos de routers
        if os.path.exists('routers.json') and os.path.getsize('routers.json') > 0:
            with open('routers.json', 'r') as f:
                self.data = json.load(f)

    def monitorear(self):


        sem = threading.Semaphore()
        mon = monitor(sem,self.data)
        mon.start()

        print("\nRouters dados de alta:\n")
        for ip in self.data:
            print("\t"+ip)

        print("\nSeleccionar una opcion:\n\n\t1.-Extraer configuracion\n\t2.-Enviar configuracion (Desde Router)\n\t3.-Enviar configuracion (Desde PC)")
        option = input()

        if option == "1":
            print("Direcciones IP (separarlas con espacios):")
            ips = input().split()
            for ip in ips:
                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                local_filename = os.path.join(r''+os.getcwd(), 'conf_'+ip)
                file = open(local_filename, 'wb')
                print("Nombre del archivo a traer de "+ip+":")
                filename = input()
                print(ftp.retrbinary('RETR '+filename , file.write))
                file.close()
                ftp.quit()

        elif option == "2":
            print("Direccion IP de router con el archivo:")
            ip = input()
            ftp = FTP(ip)
            ftp.login(user='rcp', passwd = 'rcp')
            local_filename = os.path.join(r''+os.getcwd(), 'transfer_file')
            file = open(local_filename, 'wb')
            print("Nombre del archivo a traer de "+ip+":")
            filename = input()
            print(ftp.retrbinary('RETR '+filename , file.write))
            file.close()
            ftp.quit()

            print("Direcciones IP a mandar informacion (separarlas con espacios):")
            ips = input().split()
            file = open(os.getcwd()+"/transfer_file",'rb')

            for ip in ips:
                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                print("Nombre para archivo en "+ip+":")
                destination_name = input()
                print(ftp.storbinary('STOR '+destination_name, file))
                ftp.quit()

            file.close()
            os.remove(os.getcwd()+"/transfer_file")

        elif option == "3":
            print("Archivo a mandar:")
            filename = input()
            print("Direcciones IP a mandar informacion (separarlas con espacios):")
            ips = input().split()
            for ip in ips:
                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                file = open(os.getcwd()+"/"+filename,'rb')
                print("Nombre para archivo en "+ip+":")
                destination_name = input()
                print(ftp.storbinary('STOR '+destination_name, file))
                file.close()
                ftp.quit()

        elif option == "quit":
            mon.stop = True
            quit()

rm = RouterManager()
rm.monitorear()
