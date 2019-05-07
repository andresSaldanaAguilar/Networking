import smtplib, ssl, imaplib, poplib, email
import time, threading

smtp_server = "smtp.redes3.com"
sender_email = "personada1@redes3.com"  # Enter your address
message = """SMTP_SENSOR"""
smtp_imap_time = 0.0
smtp_pop_time = 0.0
imap_time = 0.0
pop_time = 0.0
imap_total = 0.0
pop_total = 0.0

receiver_email_imap = "persona2@redes3.com"  # Enter receiver address
receiver_email_pop = "persona3@redes3.com"  # Enter receiver address
smtp =  smtplib.SMTP(smtp_server)

# Primero checamos el rendimiento de imap
smtp_start = time.time()
smtp.sendmail(sender_email, receiver_email_imap, message)
smtp_end = time.time()
smtp_imap_time =(smtp_end - smtp_start)
