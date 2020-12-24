from FECGraphClient import FECGraphClient
import json

class FECGraphSchema(object):

    node_indexes = {
        'Candidate':['CAND_ID'], 
        'Committee':['CMTE_ID'], 
        'IndivContrib':['SUB_ID']
        }

    def __init__(self):
        with open('fec.config.json') as f:
			self.config = json.load(f)
			# print self.config
			self.neo_client = FECGraphClient(self.config['neo4j']['port'],self.config['neo4j']['username'], self.config['neo4j']['password'])

    def for_real(self, parameter_list):
        pass

    def compare(self, indexes_one, indexes_two):
        return sorted(indexes_one) == sorted(indexes_two)

    def schema_is_ok(self):
        for resource_type in self.node_indexes:
            indexes = self.neo_client.graph.schema.get_indexes(resource_type)
            if not self.compare(indexes, self.node_indexes[resource_type]):
                raise Exception('Indexes do not match')
            else:
                print 'Indexes match.'

    def load_schema(self):
        with open('schema/fec.cypher') as schemaLines:
			lines =  schemaLines.readlines()
			for line in lines:
				result = self.neo_client.graph.cypher.execute(line)
				print result
                