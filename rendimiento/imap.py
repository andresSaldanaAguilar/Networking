import getpass, imaplib

#checa por l ultimo correo en el buzon
def imapSCAN():
    SERVER = "imap.redes3.com"
    USER = 'persona1'
    PASSWORD = '1234'

    M = imaplib.IMAP4(SERVER)
    M.login(USER, PASSWORD)
    M.select()
    typ, data = M.search(None, 'ALL')
    last_mail_index = len(data[0].split())
    typ, data = M.fetch(last_mail_index, '(RFC822)')

    print 'Message %s\n%s\n' % (last_mail_index, data[0][1])
    if "Esta es una prueba" in data[0][1]:
        M.store(last_mail_index,'+FLAGS','\\deleted')
        M.expunge()
        M.close()
        M.logout()
        return True
    else:
        M.close()
        M.logout()
        return False

print(imapSCAN())
