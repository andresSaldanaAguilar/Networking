
import poplib
import email

#Checa por el ultimo correo en el buzon:
#False: no ha encontrado el correo
#True: encontro el correo
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
    print(numMessages)
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

print(popSCAN())
