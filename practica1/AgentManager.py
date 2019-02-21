import json
from pprint import pprint
import os.path

class AgentManager():

    def __init__(self):
        #this dictionary carries all the existent agents
        self.data = {}
        #filling the dictionary
        if os.path.exists('agents.json') and os.path.getsize('agents.json') > 0:
            with open('agents.json', 'r') as f:
                self.data = json.load(f)  
   
    def addAgent(
		self, idAgent, hostname, version, port, comunity
	):				
        newAgent = {  
            'hostname': hostname,
            'version': version,
            'port': port,
            'comunity': comunity
        }

        self.data[str(idAgent)] = newAgent
        with open('agents.json', 'w') as f:
            json.dump(self.data, f,sort_keys=True, indent=4)

        return True

    def getAgent(
		self, idAgent
	):
        return self.data[str(idAgent)]

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
           
    