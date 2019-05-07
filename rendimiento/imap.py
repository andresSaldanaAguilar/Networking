import getpass, imaplib

#checa por l ultimo correo en el buzon
def imapSCAN():
    imap_server = "imap.redes3.com"
    user = 'persona2'
    password = '1234'

    M = imaplib.IMAP4(imap_server)
    M.login(user, password)
    M.select()
    typ, data = M.search(None, 'ALL')
    last_mail_index = len(data[0].split())
    typ, data = M.fetch(last_mail_index, '(RFC822)')

    if "SMTP_SENSOR" in data[0][1]:
        M.store(last_mail_index,'+FLAGS','\\Deleted')
        M.expunge()
        M.close()
        M.logout()
        return True
    else:
        M.close()
        M.logout()
        return False

print(imapSCAN())
