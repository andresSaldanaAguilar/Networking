import json
from pprint import pprint
import os.path
from getSNMP import *
import datetime
from createRDD import *
from updateRDD import *
from graphRDD import *
import threading

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

        updates = []
        graphs = []
        for k,v in self.data.items():

            try:  
                os.mkdir(str(k))
            except OSError:  
                print ("Creation of the directory %s failed / Already Exists" % k)
            else:  
                print ("Successfully created the directory %s " % k)

            createRDD(k+"/TCP_OUT","COUNTER")
            createRDD(k+"/TCP_IN","COUNTER")
        
        sem = threading.Semaphore()        
        for k,v in self.data.items():

            #estadisticas TCP
            
            threads.append(updateRDD(k+"/TCP_IN",v['community'],v['hostname'],'1.3.6.1.2.1.6.10.0',v['port']),sem)
            threads.append(graphRDD(k+"/TCP_IN",'total_in_tcp','','TCP IN'),sem) 

            #numero de conexiones tcp

            threads.append(updateRDD(k+"/TCP_OUT",v['community'],v['hostname'],'1.3.6.1.2.1.6.11.0',v['port']),sem)
            threads.append(graphRDD(k+"/TCP_OUT",'total_out_tcp','','TCP OUT'),sem)

        for i in range(len(threads)):
            threads[i].start()

