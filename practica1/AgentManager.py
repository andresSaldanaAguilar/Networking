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
            '1.3.6.1.2.1.1.5.0' #sysname
        )
        descr = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.1.0' #sysdescr
        )
        ifnumer = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.2.1.0' #ifnumber
        )
        uptime = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.3.0' #sysuptime
        )
        seconds = int(uptime)/100
        
        location = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.6.0' #syslocaton (physical)
        )
        contact = request(
            self.data[str(idAgent)]['community'],
            self.data[str(idAgent)]['hostname'],
            '1.3.6.1.2.1.1.4.0' #syscontact
        )
        
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
            createRDD(k+v['hostname'])
            updateRDD(k+v['hostname'],v['community'],v['hostname'],'1.3.6.1.2.1.2.2.1.10.3','1.3.6.1.2.1.2.2.1.16.3')
			graphRDD(k+v['hostname'])



    
