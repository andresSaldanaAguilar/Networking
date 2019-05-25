import os
from ftplib import FTP

#domain name or server ip:
print("Enter router IP address:")
ip = input()
ftp = FTP(ip)
ftp.login(user='rcp', passwd = 'rcp')

print("Get or Put? (g/p)")
option = input().lower()

if option == "g":
    local_filename = os.path.join(r''+os.path.dirname(os.path.realpath(__file__)), 'conf_'+ip)
    file = open(local_filename, 'wb')
    print(ftp.retrbinary('RETR startup-config' , file.write))
    file.close()
else:
    print("File to send:")
    path = input()
    file = open('/home/gabs/Documents/Github/Networking/routing/'+path,'rb')                  # file to send
    print(ftp.storbinary('STOR startup-config-test', file))     # send the file
    file.close()                                    # close file and FTP

ftp.quit()
