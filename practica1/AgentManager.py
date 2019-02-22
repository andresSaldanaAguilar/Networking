import json
from pprint import pprint
import os.path
from getMIB import *

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
        results = getMIBagent(self.data[str(idAgent)]['community'],self.data[str(idAgent)]['hostname'],self.data[str(idAgent)]['port'],'1.3.6.1.2.1.1.1.0')

	for result in results:
            print(result)

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




    
