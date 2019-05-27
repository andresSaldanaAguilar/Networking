import os
from ftplib import FTP
import json
from monitor import monitor
import threading
import datetime

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

            print('\nSeleccionar una opcion:\n\n\t1.-Extraer configuracion de router\n\t2.-Enviar configuracion (Desde Router)\n\t3.-Enviar configuracion (Desde PC)\n\t4.-Borrar una versión\n\t5.-Borrar versiones desde una fecha\n\t6.-Restaurar config de router')
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

            #eliminar una configuracion
            elif option == '4':
                for ip in self.data:
                    print('\t'+ip)
                print('Ingresar direccion del router:')
                ip = input()
                archives = os.listdir(os.getcwd()+'/'+ip)
                for archive in archives:
                    print('\t'+archive)
                print('Ingrese archivo a borrar:')
                date = input()
                os.remove(os.getcwd()+'/'+ip+'/'+date)
                print('Archivo eliminado.')

            #eliminar de una fecha en adelante configuraciones
            elif option == '5':
                for ip in self.data:
                    print('\t'+ip)
                print('Ingresar direccion del router:')
                ip = input()
                archives = os.listdir(os.getcwd()+'/'+ip)
                for archive in archives:
                    print('\t'+archive)
                print('Ingrese archivo desde cual borrar:')
                data = input()
                array = data.split('-')
                os.remove(os.getcwd()+'/'+ip+'/'+data)
                date = datetime.datetime(int(array[0]),int(array[1]),int(array[2]),int(array[3]),int(array[4]),int(array[5]))
                for archive in archives :
                    arch = archive.split('-')
                    date2  = datetime.datetime(int(arch[0]),int(arch[1]),int(arch[2]),int(arch[3]),int(arch[4]),int(arch[5]))
                    if date2 < date :
                        os.remove(os.getcwd()+'/'+ip+'/'+archive)
                print('Archivos eliminado.')

            #restaurar configuracion del router a la inicial
            elif option == '6':
                print('Ingresar direccion del router:')
                ip = input()
                ftp = FTP(ip)
                ftp.login(user='rcp', passwd = 'rcp')
                file = open(os.getcwd()+'/'+ip+'/'+firstConf(ip),'rb')
                print(ftp.storbinary('STOR startup-config', file))
                file.close()
                ftp.quit()

            #salir
            elif option == 'quit':
                mon.stop = True
                quit()

#metodo que consigue el nombre del archivo de config. mas reciente en fecha
def firstConf(ip):
    array = os.listdir(os.getcwd()+'/'+ip)
    date = None
    firstdate = None
    for item in array:
        data = item.split('-')
        date2  = datetime.datetime(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]))
        #caso base, primer archivo se vuelve el mas reciente
        if date is None:
            date = date2
            firstdate = item
        #comparamos fechas, si es mayor el archivo conseguido, se vuelve el mas reciente
        elif date2 < date:
            date = date2
            firstdate = item
    print(firstdate)
    return firstdate;

rm = RouterManager()
rm.monitorear()
