#A cache is maintained in case of allocation type of features;
#A first level cache key gets created for each type of allocation feature 
#This key references unique keys built from input params to allocation feature 
#These keys reference objects containing all output params of feature query string
#Example: 
#CacheKey: APercent#BPercent
#DataKey: {2#3:{'APercent':0.1,'BPercent':0.3}}
#{'APercent#BPercent':{2#3:{'APercent':0.1,'BPercent':0.3}}}

class Cache:
	def __init__(self):
		self.allFeaturesData={}

	#make an entry for this data in Allocation Cache
	#dataDictionary:dictionary of output params
	def saveData(self,featureName,inputParamValList,dataDictionary):
		from Utils.DataUtils import DataUtils
		"""inputParamList=[]
		inputParamValList=[]
		for tupleVal in inputParamTuple:
			inputParamList.append(tupleVal[0])
			inputParamValList.append(tupleVal[1]) 
		"""
		inputKeyList=[]
		inputKeyList.append(featureName)
		"""for inputParam in inputParamList:
			inputKeyList.append(inputParam)"""
		featureKey=DataUtils.getUniqueKey(inputKeyList)
		inputParamListKey=DataUtils.getUniqueKey(inputParamValList)
		thisFeatureDict={}
		#Check if this feature has been cached before 
		if self.allFeaturesData.has_key(featureKey) is True:
			thisFeatureDict=self.allFeaturesData[featureKey]
			#Check if this input params set has been cached before
			if thisFeatureDict.has_key(inputParamListKey) is False:
				#Putting new entry
				thisFeatureDict[inputParamListKey]=dataDictionary
			else:
				#Replacing current entry
				thisFeatureDict[inputParamListKey]=dataDictionary
			self.allFeaturesData[featureKey]=thisFeatureDict
		else:
			thisFeatureDict={}
			thisFeatureDict[inputParamListKey]=dataDictionary
			self.allFeaturesData[featureKey]=thisFeatureDict


	#Fetch data for a set of featureKey and dataKey
	def getData(self,featureName,inputParamValList):
		from Utils.DataUtils import DataUtils
		"""inputParamList=[]
		inputParamValList=[]
		print inputParamTuple
		for tupleVal in inputParamTuple:
			inputParamList.append(tupleVal[0])
			inputParamValList.append(tupleVal[1]) 
		"""
		inputKeyList=[]
		inputKeyList.append(featureName)
		"""for inputParam in inputParamList:
			inputKeyList.append(inputParam)
		"""
		featureKey=DataUtils.getUniqueKey(inputKeyList)
		dataKey=DataUtils.getUniqueKey(inputParamValList)
		if self.allFeaturesData.has_key(featureKey) is True:
			featureDataList=self.allFeaturesData[featureKey]
			if featureDataList.has_key(dataKey) is True:
				return featureDataList[dataKey]
		return None

