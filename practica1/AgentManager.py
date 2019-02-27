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
            #trafico interfaz
            createRDD("interface"+k,2)
            u = updateRDD("interface"+k,v['community'],v['hostname'],'1.3.6.1.2.1.2.2.1.10.3','1.3.6.1.2.1.2.2.1.16.3',v['port'])
            g = graphRDD("interface"+k,'inoctects','outoctecs','Bytes/s')
            u.start()
            g.start()
            
            #numero de conexiones tcp
            createRDD("conexiones_tcp"+k,1)
            u2 = updateRDD("conexiones_tcp"+k,v['community'],v['hostname'],'1.3.6.1.2.1.6.9.0',None,v['port'])
            g2 = graphRDD("conexiones_tcp"+k,'Conexiones TCP establecidas',None,'no. conexiones')
            u2.start()
            g2.start()
            
            #estadisticas ICMP
            createRDD("ICMP"+k,2)
            u3 = updateRDD("ICMP"+k,v['community'],v['hostname'],'1.3.6.1.2.1.5.1.0','1.3.6.1.2.1.5.14.0',v['port'])
            g3 = graphRDD("ICMP"+k,'total_in_icmp','total_out_icmp','')
            u3.start()
            g3.start()
            
            #estadisticas SNMP
            createRDD("SNMP"+k,2)
            u3 = updateRDD("SNMP"+k,v['community'],v['hostname'],'1.3.6.1.2.1.5.1.0','1.3.6.1.2.1.5.14.0',v['port'])
            g3 = graphRDD("SNMP"+k,'total_in_snmp','total_out_snmp','')
            u3.start()
            g3.start()
            
            #estadisticas TCP
            createRDD("TCP"+k,2)
            u3 = updateRDD("TCP"+k,v['community'],v['hostname'],'1.3.6.1.2.1.6.10.0','1.3.6.1.2.1.6.11.0',v['port'])
            g3 = graphRDD("TCP"+k,'total_in_tcp','total_out_tcp','')
            u3.start()
            g3.start()
            



    
