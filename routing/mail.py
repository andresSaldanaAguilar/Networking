import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class mail(object):

    def __init__(self,asunto,path1,path2,filename1,filename2):
        self.msg = MIMEMultipart()
        self.msg['Subject'] = asunto
        self.msg['From'] = 'example@gmail.com'
        self.msg['To'] = 'destination@gmail.com'

        #adjuntamos el primer archivo (antes del cambio)
        f1 = MIMEBase('application', "octet-stream")
        f1.set_payload(open(path1, "rb").read())
        encoders.encode_base64(f1)
        f1.add_header('Content-Disposition', 'attachment; filename="'+filename1+'.txt"')
        self.msg.attach(f1)

        #adjuntamos el segundo archivo (despues del cambio)
        f2 = MIMEBase('application', "octet-stream")
        f2.set_payload(open(path2, "rb").read())
        encoders.encode_base64(f2)
        f2.add_header('Content-Disposition', 'attachment; filename="'+filename2+'.txt"')
        self.msg.attach(f2)


    def sendMail(self):
        mserver = smtplib.SMTP('smtp.gmail.com: 587')
        mserver.starttls()
        mserver.login('example@gmail.com', '')
        mserver.sendmail('example@gmail.com', 'destination@gmail.com', self.msg.as_string())
        mserver.quit()
