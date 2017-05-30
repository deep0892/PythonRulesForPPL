from Generator.models import *

#Used to fetch information about features,namely
#Query Strings
#Feature Type(LEAD,AGENT,ALLOCATION)
#
class FeatureStore:
	QSrepo='/home/policy/Sanket/02Sources/triumphAttempts/triumph2/triumph2/Utils/QueryStrings1.json'
	def __init__(self):
		pass
	
	#Returns Query String corresponding to a feature	
	def getFeatureQS(self,featureNameArg):
		import json
		with open(FeatureStore.QSrepo) as data_file:
			data=json.load(data_file)
		featureEntry=data[str(featureNameArg)]
		if featureEntry['queryString']!='None':
			return featureEntry['queryString']
		else:
			return None
	
	#Returns Feature Type for a feature(ALLOCATION/LEAD/AGENT)	
	def getFeatureType(self,featureNameArg):
		#print 'getFeatureType function called with argument '+str(featureNameArg)
		import json
		with open(FeatureStore.QSrepo) as data_file:
			data=json.load(data_file)
		featureEntry=data[str(featureNameArg)]
		return featureEntry['type']
		
	#Returns Complete Feature data for a feature
	def getFeatureData(self,featureNameArg):
		import json
		with open(FeatureStore.QSrepo) as data_file:
			data=json.load(data_file)
		return data[str(featureNameArg)]

	#Save a feature information in json format
	def saveFeatureQuery(self,featureNameArgList,featureQueryString,featureTypeString):
		import json,os
		jsonFile=FeatureStore.QSrepo
		jsonData =None
		if os.path.exists(jsonFile):
			with open(jsonFile) as data_file:
				data=json.load(data_file)
			jsonData=data		
		else:
			data={}
		
		newFeature={}
		newFeature['queryString']=featureQueryString
		newFeature['type']=featureTypeString
		newFeature['featureList']=featureNameArgList
	
		for featureNameArg in featureNameArgList:
			data[featureNameArg]=newFeature	
				
			with open(jsonFile,'w') as data_file:
				json.dump(data,data_file)
	

	#Not being used currently to be used when feature query strings are to be determined automatically using schema information
	def buildQuery(self,featureNameArg):
		#Not being used currently
		#Fetch feature details;Compose query through joins;Fetch Data
		listOfFeatures=Feature.objects(featureName=featureNameArg)
		for feature in listOfFeatures:
			break
		if feature.propertyType == 'LEAD':
			listOfTables=Table.objects(tableName=feature.tableName)	
			for table in listOfTables:
				print table.attributes
				print table.relations
				print table.relationPaths
				print table.tableName
				relationPath=table.relationPaths
				break
			selectQuery='SELECT  '
			selectQuery=selectQuery+' FROM '+table.tableName +' with (nolock) '
			for node in relationPath:
				print 'Node of relation path is ----------- '
				print str(node.tableName)
				print str(node.attributeName)
	
			#print 'in lead property type'
			#print table
			pass
		elif feature.propertyType == 'AGENT':		
			print 'in agent property type'
			pass
		elif feature.propertyType == 'ALLOCATION':
			print 'in allocation property type'
			pass
		
