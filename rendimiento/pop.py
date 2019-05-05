
import poplib
import email


SERVER = "pop3.redes3.com"
USER = 'persona1'
PASSWORD = '1234'


server = poplib.POP3(SERVER,110)
print(server.user(USER))
print(server.pass_(PASSWORD))


numMessages = len(server.list()[1])
print(numMessages)
(server_msg, body, octets) = server.retr(numMessages)
for j in body:
    try:
        msg = email.message_from_string(j.decode("utf-8"))
        strtext=msg.get_payload()
        print (strtext)
    except:
        pass
