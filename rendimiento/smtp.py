import smtplib, ssl, imaplib, poplib, email
import time, threading

class SMTP_SENSOR():
    def __init__(self):
        self.smtp_server = "smtp.redes3.com"
        self.sender_email = "smtp@redes3.com"
        self.message = """SMTP_SENSOR"""
        self.smtp_imap_time = 0.0
        self.smtp_pop_time = 0.0
        self.imap_time = 0.0
        self.pop_time = 0.0
        self.imap_total = 0.0
        self.pop_total = 0.0

    def scan_smtp(self):
        receiver_email_imap = "persona2@redes3.com"
        receiver_email_pop = "persona3@redes3.com"
        smtp =  smtplib.SMTP(self.smtp_server)

        # Primero checamos el rendimiento de imap
        try:
            smtp_start = time.time()
            smtp.sendmail(self.sender_email, receiver_email_imap, self.message)
            smtp_end = time.time()
            self.smtp_imap_time =(smtp_end - smtp_start)
        except:
            self.smtp_imap_time = "down"

        imap_tries = 0
        imap_start = time.time()
        while(not imapSCAN()):
            #waiting for email to come to imap client
            if(imap_tries > 4):
                break
            imap_tries = imap_tries+1

        if(imap_tries > 4):
            self.imap_total = "down"
            self.imap_time = "down"
        else:
            imap_end = time.time()
            self.imap_time =(imap_end - imap_start)
            #total
            self.imap_total = self.smtp_imap_time + self.imap_time


        #####################################################################

        #Ahora, checamos el rendimiento de pop
        try:
            smtp_start = time.time()
            smtp.sendmail(self.sender_email, receiver_email_pop, self.message)
            smtp_end = time.time()
            self.smtp_pop_time =(smtp_end - smtp_start)
        except:
            self.smtp_pop_time = "down"

        pop_tries = 0
        pop_start = time.time()
        while(not popSCAN()):
            #waiting for email to come to pop client
            if(pop_tries > 4):
                break
            pop_tries = pop_tries+1

        if(pop_tries > 4):
            self.imap_total = "down"
            self.imap_time = "down"
        else:
            pop_end = time.time()
            self.pop_time =(pop_end - pop_start)
            #total
            self.pop_total = self.smtp_pop_time + self.pop_time

        smtp.quit()



#Checa por el ultimo correo en el buzon:
#False: no ha encontrado el correo
#True: encontro el correo
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

def popSCAN():
    pop_server = "pop3.redes3.com"
    user = 'persona3'
    password = '1234'
    return_value = False

    pop_server = poplib.POP3(pop_server,110)
    pop_server.user(user)
    pop_server.pass_(password)

    numMessages = len(pop_server.list()[1])
    server_msg, body, octets = pop_server.retr(numMessages)
    for j in body:
        try:
            msg = email.message_from_string(j.decode("utf-8"))
            msg_text = msg.get_payload()
            if "SMTP_SENSOR" in msg_text:
                return_value = True
                pop_server.dele(numMessages)
        except:
            pass

    pop_server.quit()
    return return_value



sensor = SMTP_SENSOR()

while(True):
    sensor.scan_smtp()
    print(sensor.imap_total)
    print(sensor.imap_total)
    time.sleep(2)
