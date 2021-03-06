import json
from pprint import pprint
import os.path
from getSNMP import *
import datetime
from createRDD import *
from updateRDD import *
from graphRDD import *

class AgentManager():

    def __init__(self):
        #this dictionary carries all the existent agents
        self.data = {}
        self.pool = {}
        #filling the dictionary
        if os.path.exists('agents.json') and os.path.getsize('agents.json') > 0:
            with open('agents.json', 'r') as f:
                self.data = json.load(f)  

    def addAgent(
        self, idAgent, hostname, version, port, community
    ):				
        newAgent = {  
            'hostname': hostname,
            'version': version,
            'port': port,
            'community': community
        }

        self.data[str(idAgent)] = newAgent
        with open('agents.json', 'w') as f:
            json.dump(self.data, f,sort_keys=True, indent=4)

        return True

    def getMIBAgent(
        self, idAgent
    ):
        name = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.5.0', #sysname
            self.data[str(idAgent)]['port']
        )
        descr = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.1.0', #sysdescr
            self.data[str(idAgent)]['port']
        )
        ifnumer = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.2.1.0', #ifnumber
            self.data[str(idAgent)]['port']
        )
        uptime = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.3.0', #sysuptime
            self.data[str(idAgent)]['port']
        )
        if(uptime != ""):
            seconds = int(uptime)/100
        
        location = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.6.0', #syslocaton (physical)
            self.data[str(idAgent)]['port']
        )
        contact = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.4.0', #syscontact
            self.data[str(idAgent)]['port']
        )
        
        if(uptime != ""):
            print("--------------- Agent info  -----------------------")
            print("Host: "+self.data[str(idAgent)]['hostname'])
            print("Name: "+name)
            print("Version: "+self.data[str(idAgent)]['version'])
            print("Description: "+descr)
            print("Number of interfaces: "+ifnumer)
            print("Up since: " + str(datetime.timedelta(seconds=seconds)))
            print("Location: "+location)
            print("Contact: "+contact)
            print("---------------------------------------------------")
        else:
            print("--------------- No Agent info  -----------------------")

    def removeAgent(
        self, idAgent
    ):
        del self.data[str(idAgent)]
        with open('agents.json', 'w') as f:
            json.dump(self.data, f,sort_keys=True, indent=4)

        return True

    def readJson(
        self
    ):
        with open('agents.json') as f:
            self.data = json.load(f)
            pprint(self.data)
            
    def agentMonitoring(
        self
    ):
        for k,v in self.data.items():

            try:  
                os.mkdir(str(k))
            except OSError:  
                print ("Creation of the directory %s failed / Already Exists" % k)
            else:  
                print ("Successfully created the directory %s " % k)

			#counter te guarda en el rrd la diferencia entre el valor pasado y el actual, gauge el valor crudo
			
            #trafico interfaz
            createRDD(k+"/interface",2,"GAUGE")
            u = updateRDD(k+"/interface",v['community'],v['hostname'],'1.3.6.1.2.1.2.2.1.10.3','1.3.6.1.2.1.2.2.1.16.3',v['port'])
            g = graphRDD(k+"/interface",'inoctects','outoctecs','Bytes/s','Trafico de interfaz')
            u.start()
            g.start()
            
            #numero de conexiones tcp
            createRDD(k+"/conexiones_tcp",1,"GAUGE")
            u2 = updateRDD(k+"/conexiones_tcp",v['community'],v['hostname'],'1.3.6.1.2.1.6.9.0',None,v['port'])
            g2 = graphRDD(k+"/conexiones_tcp",'Conexiones TCP establecidas',None,'no. conexiones','Conexiones TCP')
            u2.start()
            g2.start()
            
            #estadisticas ICMP
            createRDD(k+"/ICMP",2,"GAUGE")
            u3 = updateRDD(k+"/ICMP",v['community'],v['hostname'],'1.3.6.1.2.1.5.1.0','1.3.6.1.2.1.5.14.0',v['port'])
            g3 = graphRDD(k+"/ICMP",'total_in_icmp','total_out_icmp','','Estadisticas ICMP')
            u3.start()
            g3.start()
            
            #estadisticas SNMP
            createRDD(k+"/SNMP",2,"GAUGE")
            u4 = updateRDD(k+"/SNMP",v['community'],v['hostname'],'1.3.6.1.2.1.5.1.0','1.3.6.1.2.1.5.14.0',v['port'])
            g4 = graphRDD(k+"/SNMP",'total_in_snmp','total_out_snmp','','Estadisticas SNMP')
            u4.start()
            g4.start()
            
            #estadisticas TCP
            createRDD(k+"/TCP",2,"GAUGE")
            u5 = updateRDD(k+"/TCP",v['community'],v['hostname'],'1.3.6.1.2.1.6.10.0','1.3.6.1.2.1.6.11.0',v['port'])
            g5 = graphRDD(k+"/TCP",'total_in_tcp','total_out_tcp','','estadisticas TCP')
            u5.start()
            g5.start()
            



    
