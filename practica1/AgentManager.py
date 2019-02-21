import json

class AgentManager():
    def __init__(self):
        self.data = {}
        self.data['agents'] = [] 

    def addAgent(
		self, idAgent, hostname, version, port, comunity
	):		
		
		#if idAgent in self.pool:
		#	return False		

        newAgent = {  
            'idAgent': idAgent,
            'hostname': hostname,
            'version': version,
            'port': port,
            'comunity': comunity
        }

        self.data['agents'].append(newAgent)
        with open('agents.json', 'w') as f:
            json.dump(self.data, f)

        return True

    def addAgent(
		self, idAgent
	):