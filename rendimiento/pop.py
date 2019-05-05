
import poplib
import email


SERVER = "server_name"   
USER = 'andres.saldana.aguilar@gmail.com' 
PASSWORD = 'Keane000110'
 

server = poplib.POP3_SSL('pop.googlemail.com', '995') 
server.user(USER)
server.pass_(PASSWORD)
 
 
numMessages = len(server.list()[1])
if (numMessages > 15):
    numMessages=1
for i in range(numMessages) :
    (server_msg, body, octets) = server.retr(i+1)
    for j in body:
        try:
            msg = email.message_from_string(j.decode("utf-8"))
            strtext=msg.get_payload()
            print (server_msg)
        except:
            pass