import smtplib, ssl
import time

smtp_server = "smtp.redes3.com"
sender_email = "persona2@redes3.com"  # Enter your address
receiver_email = "persona1@redes3.com"  # Enter receiver address
password = "1234"
message = """\
Subject: Hola

Esta es una prueba"""


server =  smtplib.SMTP(smtp_server)
start = time.time()
server.sendmail(sender_email, receiver_email, message)
print(server.quit())
end = time.time()
print(end - start)
