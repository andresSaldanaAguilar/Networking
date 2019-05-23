from ftplib import FTP

#domain name or server ip:
ftp = FTP('10.22.0.2')
print(ftp.login(user='rcp', passwd = 'rcp'))
