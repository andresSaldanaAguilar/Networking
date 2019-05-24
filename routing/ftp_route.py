import os
from ftplib import FTP

#domain name or server ip:
print("Enter router IP to extract config:")
ip = str(input())
ftp = FTP(ip)
ftp.login(user='rcp', passwd = 'rcp')

local_filename = os.path.join(r'/home/andres/Desktop', 'conf_'+ip)
handle = open(local_filename, 'wb')
ftp.retrbinary('RETR %s' % 'startup-config', handle.write)


