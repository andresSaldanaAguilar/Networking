from AgentManager import AgentManager

am = AgentManager()

        
def main():
    print("SNMP Monitor")
    menu()

def menu():
    am.agentMonitoring()
    while 1:
        #mostrar por cada agente: status (up o down), interfaces y su estatus 
        am.readJson()
        print("1. Agregar Agente")
        print("2. Eliminar Agente")
        print("3. Estado de un Agente")
        print("4. Salir")
        opc = int(input())
        if opc == 1:
            agentID = input("agentID: ")
            hostname = input("Hostname/IP: ")
            version = input("Version: ")
            port = int(input("Port: "))
            community = input("Community: ")
            os = input("OS (w/l): ")

            if am.addAgent(
                agentID, hostname, version, port, community, os
            ):
                print(agentID + " registrado.")
            else:
                print("Ya existe el agentID.")

        if opc == 2:
            agentID = input("agentID: ")
            if am.removeAgent(agentID):
                print(agentID + " eliminado.")
            else:
                print("No se encontro el agentID.")

        if opc == 3:
            agentID = input("agentID: ")
            agent = am.getMIBAgent(agentID)
            print(agent)
            
        if opc == 4:
            print("Cerrando monitores.")
            break

main()
