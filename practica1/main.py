#from AgentManager import AgentManager

#mm = AgentManager()

        
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
		opc = input()

		if opc == 1:
			idAgente = raw_input("IdAgente: ")
			hostname = raw_input("Hostname: ")
			version = raw_input("Version: ")
			port = int(raw_input("Port: "))
			comunity = raw_input("Comunity: ")

			ramReady = 800000000
			ramSet = 700000000
			ramGo = 600000000
			cpuReady = 20
			cpuSet = 60
			cpuGo = 90
			hddReady = 5500000
			hddSet = 6000000
			hddGo = 7000000

			confOpc = raw_input("Desea configurar los umbrales de rendimiento? s/n")
			if confOpc == "s":
				ramReady = raw_input("RAM (ready): ")
				ramSet = raw_input("RAM (set): ")
				ramGo = raw_input("RAM (go): ")
				cpuReady = raw_input("CPU (ready): ")
				cpuSet = raw_input("CPU (set): ")
				cpuGo = raw_input("CPU (go): ")
				hddReady = raw_input("HDD (ready): ")
				hddSet = raw_input("HDD (set): ")
				hddGo = raw_input("HDD (go): ")

			if mm.addAgent(
				idAgente, hostname, version, port, comunity,
				ramReady, ramSet, ramGo,
				cpuReady, cpuSet, cpuGo,
				hddReady, hddSet, hddGo
			):
				print(idAgente + " registrado.")
			else:
				print("Ya existe el idAgente.")



		if opc == 2:
			idAgente = raw_input("IdAgente: ")
			if mm.removeAgent(idAgente):
				print(idAgente + " eliminado.")
			else:
				print("No se encontro el idAgente.")


		if opc == 3:
			idAgente = raw_input("IdAgente: ")
			if not mm.consulta(idAgente):
				print("No se encontro el idAgente.")
			

		if opc == 4:
			continue;

		if opc == 6:
			print("Cerrando monitores.")
			break;

main()