import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configurations import mailsender,mailreceip,password,mailserver

class enviaMail(object):
    
    def __init__(self):
        pass

    def armaMail(self,asunto,filename):
        
        self.msg = MIMEMultipart()
        self.msg['Subject'] = asunto
        self.msg['From'] = mailsender
        self.msg['To'] = mailreceip
        #we attach the photo to the mail
        fp = open(filename+'.png', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        self.msg.attach(img)

    def enviaMail(self):
        try:
            mserver = smtplib.SMTP(mailserver)
            mserver.starttls()
            # Login Credentials for sending the mail
            mserver.login(mailsender, password)
            mserver.sendmail(mailsender, mailreceip, self.msg.as_string())
            mserver.quit()
            print("email enviado")
        except:
            print("email no enviado")

        