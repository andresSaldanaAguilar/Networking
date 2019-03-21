import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from configurations import mailsender,mailreceip,password,mailserver

def checkErrors(valor, umbral):
    try:
        if float(valor) >= umbral:
            return True
        else:
            return False
    except:
        return False

def sendEmail(foto, tipo):
    try:
        #we create the email, and we substract the information of the sender from the configurations file
        subject = "Notificación de rebaso de umbral de "+tipo+" equipo3 grupo 4CM1"
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = mailsender
        msg['To'] = mailreceip
        #we attach the photo to the mail
        fp = open(foto+'.png', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        #we create the object of the mail
        mserver = smtplib.SMTP(mailserver)
        mserver.starttls()
        # Login Credentials for sending the mail
        mserver.login(mailsender, password)
        mserver.sendmail(mailsender, mailreceip, msg.as_string())
        mserver.quit()
        print("email sent")
    except:
        print("email not sent")

