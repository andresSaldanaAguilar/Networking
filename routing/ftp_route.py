import os
from ftplib import FTP

#domain name or server ip:


print("Seleccionar una opcion:\n1.-Extraer configuracion\n2.-Enviar configuracion (Router)\n3.-Enviar configuracion (PC)")
option = input()

if option == "1":
    print("Direcciones IP (separarlas con espacios):")
    ips = input().split()
    for ip in ips:
        ftp = FTP(ip)
        ftp.login(user='rcp', passwd = 'rcp')
        local_filename = os.path.join(r''+os.path.dirname(os.path.realpath(__file__)), 'conf_'+ip)
        file = open(local_filename, 'wb')
        print(ftp.retrbinary('RETR startup-config' , file.write))
        file.close()
        ftp.quit()

elif option == "2":
    print("Direccion IP de router con el archivo:")
    ip = input()
    ftp = FTP(ip)
    ftp.login(user='rcp', passwd = 'rcp')
    local_filename = os.path.join(r''+os.path.dirname(os.path.realpath(__file__)), 'transfer_file')
    file = open(local_filename, 'wb')
    print(ftp.retrbinary('RETR startup-config' , file.write))
    file.close()
    ftp.quit()

    print("Direcciones IP a mandar informacion (separarlas con espacios):")
    ips = input().split()
    for ip in ips:
        ftp = FTP(ip)
        ftp.login(user='rcp', passwd = 'rcp')
        file = open(os.path.dirname(os.path.realpath(__file__))+"/"+filename,'rb')
        print("Nombre para archivo en "+ip+":")
        destination_name = input()
        print(ftp.storbinary('STOR '+destination_name, file))
        file.close()
        ftp.quit()

    os.remove(os.path.dirname(os.path.realpath(__file__))+"/transfer_file")

elif option == "3":
    print("Archivo a mandar:")
    filename = input()
    print("Direcciones IP a mandar informacion (separarlas con espacios):")
    ips = input().split()
    for ip in ips:
        ftp = FTP(ip)
        ftp.login(user='rcp', passwd = 'rcp')
        file = open(os.path.dirname(os.path.realpath(__file__))+"/"+filename,'rb')
        print("Nombre para archivo en "+ip+":")
        destination_name = input()
        print(ftp.storbinary('STOR '+destination_name, file))
        file.close()
        ftp.quit()
