"""
Compose queries for a feature based on input data, fetch data from sql server

"""
class FeatureExec:
	TAG='FeatureExec'
	def __init__(self):
		pass
	
	def fetchFeatureValue(self,featureName,inputProperties):
		from Utils.Log import Log
		from FeatureManager.FeatureStore import FeatureStore
		from Utils.TriumphKey import TriumphKey
		fs=FeatureStore()
		#print 'fetch Feature value is -------------------------'
		queryString=fs.getFeatureQS(featureName)
		if queryString == None:
			return None	
		if inputProperties[TriumphKey.FeatureFetchProperty.dataType] == TriumphKey.FeatureType.LEAD:
			whereSearchString='where'
			groupBySearchString='group by'
			if inputProperties[TriumphKey.FeatureFetchProperty.inputDataField] == TriumphKey.LeadInputDataField.leadId:
				wherePosIndex=queryString.lower().find(whereSearchString)+len(whereSearchString)
				leadIdListString='('
				for leadId in inputProperties[TriumphKey.FeatureFetchProperty.data]:
					leadIdListString+=str(leadId)+','
				leadIdListString=leadIdListString[0:-1]+')'
				leadIdInsertionString=' ld.leadId IN '+str(leadIdListString)
				if wherePosIndex > len(whereSearchString):
					lenCurrentQuery=len(queryString)
					queryString=queryString[0:wherePosIndex]+leadIdInsertionString+' AND '+queryString[wherePosIndex:lenCurrentQuery]								
				else:					
					lenCurrentQuery=len(queryString)
					groupByPosIndex=queryString.lower().find(groupBySearchString)
					if groupByPosIndex > len(groupBySearchString):
						queryString=queryString[0:groupByPosIndex]+' WHERE '+leadIdInsertionString+queryString[groupByPosIndex:lenCurrentQuery]
					else:
						queryString=queryString[0:lenCurrentQuery]+' WHERE '+leadIdInsertionString
				#print queryString							
			elif inputProperties[TriumphKey.FeatureFetchProperty.inputDataField]==TriumphKey.LeadInputDataField.mobileNo:
				pass				
		elif inputProperties[TriumphKey.FeatureFetchProperty.dataType] == TriumphKey.FeatureType.AGENT:
			pass
		elif inputProperties[TriumphKey.FeatureFetchProperty.dataType] == TriumphKey.FeatureType.ALLOCATION:
			inputTuple=inputProperties[TriumphKey.FeatureFetchProperty.data]
			queryString=queryString%inputTuple
			
		from Utils.dbAdapter import dbAdapter
		dbAdapter=dbAdapter('REPLICASQL')		
		resultsList=dbAdapter.fetchData(queryString)
		return resultsList
		
