import smtplib, ssl
import time

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "andres.saldana.aguilar@gmail.com"  # Enter your address
receiver_email = "pollyketpo@gmsfsfil.com"  # Enter receiver address
password = "Keane000110"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    start = time.time()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    print(server.quit())
    end = time.time()
    print(end - start)
