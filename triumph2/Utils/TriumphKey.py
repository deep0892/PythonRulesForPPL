class TriumphKey:
	from enum import Enum
	class OperandType(Enum):
		LITERAL='literal'
		VAR='var'
		FEATURE='feature'
		OPERATION='operation'

	class FeatureType(Enum):
		AGENTID='AGENT'
		LEADID='LEAD'
		ALLOCATIONID='ALLOCATION'
		AGENT='AGENT'
		LEAD='LEAD'
		ALLOCATION='ALLOCATION'
	
	class MongoParams(Enum):
		DB_NAME='testdb'
		PORT=27017
		HOST='127.0.0.1'

	class Operator(Enum):
		EQUALS='equals'
		LT='lt'
		GT='gt'
		LE='le'
		GE='ge'
		NE='ne'
		AND='and'
		OR='or'
		NOT='not'
		SET='set'
		SUBRULE='subRule'
		FEATURE='feature'			
		LOOP='loop'
		ADD='add'
		PRODUCT='product'
		SUBTRACT='subtract'
		DIVIDE='divide'

	class SORTORDER(Enum):
		ASC='ASC'
		DESC='DESC' 	
	
	class FeatureFetchProperty(Enum):
		dataType='dataType'
		inputDataField='inputDataField'
		data='data'	

	class LeadInputDataField(Enum):
		leadId='leadId'
		mobileNo='mobileNo'				 
	
	@classmethod 
	def init(cls):
		pass	
