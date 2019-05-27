import os
from ftplib import FTP
import json
from monitor import monitor
import threading

class RouterManager():

    def __init__(self):
        #diccionario para routers
        self.data = {}
        #extrayndo base de datos de routers
        if os.path.exists('routers.json') and os.path.getsize('routers.json') > 0:
            with open('routers.json', 'r') as f:
                self.data = json.load(f)

    def monitorear(self):

        #semaforo para el control de acceso a recursos compartidos
        sem = threading.Semaphore()
        #hilo que monitorea los archivos de configuracion
        mon = monitor(sem,self.data)
        mon.start()

        #menu del programa
        while True:

            print('\nRouters dados de alta:\n')
            for ip in self.data:
                print('\t'+ip)

            print('\nSeleccionar una opcion:\n\n\t1.-Extraer configuracion de router\n\t2.-Enviar configuracion (Desde Router)\n\t3.-Enviar configuracion (Desde PC)\n\t4.-Borrar configuracion de version')
            option = input()

            #extraer la configuracion de uno o mas routers
            if option == '1':
                print('Direcciones IP (separarlas con espacios):')
                ips = input().split()
                for ip in ips:
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    local_filename = os.path.join(r''+os.getcwd(), 'conf_'+ip)
                    file = open(local_filename, 'wb')
                    print('Nombre del archivo a traer de '+ip+':')
                    filename = input()
                    print(ftp.retrbinary('RETR '+filename , file.write))
                    file.close()
                    ftp.quit()

            #enviar configuracion desde un router a otro
            elif option == '2':
                print('Direccion IP de router con el archivo:')
                ip = input()
                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                local_filename = os.path.join(r''+os.getcwd(), 'transfer_file')
                file = open(local_filename, 'wb')
                print('Nombre del archivo a traer de '+ip+':')
                filename = input()
                print(ftp.retrbinary('RETR '+filename , file.write))
                file.close()
                ftp.quit()

                print('Direcciones IP a mandar informacion (separarlas con espacios):')
                ips = input().split()
                file = open(os.getcwd()+'/transfer_file','rb')

                for ip in ips:
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    print('Nombre para archivo en '+ip+':')
                    destination_name = input()
                    print(ftp.storbinary('STOR '+destination_name, file))
                    ftp.quit()

                file.close()
                os.remove(os.getcwd()+'/transfer_file')

            #enviar configuracion de la compu a otros routers
            elif option == '3':
                print('Archivo a mandar:')
                filename = input()
                print('Direcciones IP a mandar informacion (separarlas con espacios):')
                ips = input().split()
                for ip in ips:
                    ftp = FTP(ip)
                    ftp.login(user='rcp', passwd = 'rcp')
                    file = open(os.getcwd()+'/'+filename,'rb')
                    print('Nombre para archivo en '+ip+':')
                    destination_name = input()
                    print(ftp.storbinary('STOR '+destination_name, file))
                    file.close()
                    ftp.quit()

            #enviar configuracion de la compu a otros routers
            elif option == '4':
                for ip in self.data:
                    print('\t'+ip)
                print('Ingresar direccion del router:')
                ip = input()
                archives = os.listdir(os.getcwd()+'/'+ip)
                for archive in archives:
                    print('\t'+archive)
                print('Ingresa fecha de archivo a borrar')
                date = input()
                os.remove(os.getcwd()+'/'+ip+'/'+date)
                print('Archivo eliminado.')

            #salir
            elif option == 'quit':
                mon.stop = True
                quit()

rm = RouterManager()
rm.monitorear()
