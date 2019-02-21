from AgentManager import AgentManager

mm = AgentManager()

        
def main():
	print("SNMP Monitor")
	menu()

def menu():
    while 1:
        #mostrar por cada agente: status (up o down), interfaces y su estatus 
        print("1. Agregar Agente")
        print("2. Eliminar Agente")
        print("3. Estado de un agente")
        print("4. Graficas de un agente")
        print("5. Salir")
        opc = int(input())
        if opc == 1:
            idAgente = input("IdAgente: ")
            hostname = input("Hostname: ")
            version = input("Version: ")
            port = int(input("Port: "))
            comunity = input("Comunity: ")

            if mm.addAgent(
                idAgente, hostname, version, port, comunity
            ):
                print(idAgente + " registrado.")
            else:
                print("Ya existe el idAgente.")

        if opc == 2:
            idAgente = input("IdAgente: ")
            if mm.removeAgent(idAgente):
                print(idAgente + " eliminado.")
            else:
                print("No se encontro el idAgente.")

        if opc == 3:
            #idAgente = input("IdAgente: ")
            mm.readJson()
            
        if opc == 4:
            continue;

        if opc == 5:
            print("Cerrando monitores.")
            break;

main()