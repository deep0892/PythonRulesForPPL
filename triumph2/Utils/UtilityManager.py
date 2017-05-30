class UtilityManager:

	#Enum containing listing of names of utility classes
	from enum import Enum
	class SupportedUtils(Enum):
		GeneralUtils='GeneralUtils'
		AssignmentUtils='AssignmentUtils'

	#constructor contains objects of all utility classes
	def __init__(self):
		#Objects of utility classes to be referenced later through a dictionary 
		from Utils.GeneralUtils import GeneralUtils
		from Utils.AssignmentUtils import AssignmentUtils
		self.generalUtilsObj=GeneralUtils()
		self.assignmentUtilsObj=AssignmentUtils()		
		#Dictionary entry containing all operations supported by a class against classname as a key
		self.supportedOps={}
		generalUtilsOps=[GeneralUtils.UtilKey.SORT]
		assignmentUtilsOps=[AssignmentUtils.UtilKey.ASSIGN]
		self.supportedOps[UtilityManager.SupportedUtils.GeneralUtils]=generalUtilsOps
		self.supportedOps[UtilityManager.SupportedUtils.AssignmentUtils]=assignmentUtilsOps
		#Mapping of rule strings for utilities to enum value being used in Utility classes
		self.ruleStringUtilMap={}
		self.ruleStringUtilMap['sort']=GeneralUtils.UtilKey.SORT
		self.ruleStringUtilMap['assign']=AssignmentUtils.UtilKey.ASSIGN

	#Function returns Utility class object for enum param arg passed
	#keyString is key identifying Utility class containing a utility
	def getObjectForKey(self,keyString):
		if keyString==UtilityManager.SupportedUtils.GeneralUtils:
			return self.generalUtilsObj
		elif keyString==UtilityManager.SupportedUtils.AssignmentUtils:
			return self.assignmentUtilsObj

	#Searchs SupportedOps dictionary to find out className for the operation passed as argument
	def getClassKeyForOperation(self,operation):
		for key,value in self.supportedOps.iteritems():
			if operation in value:
				return key

	#Static class method to fetch utilityManager to ensure that all utility classes remain singleton
	@classmethod
	def getUtilityManager(cls):
		if not hasattr(UtilityManager,'utilityManagerObj'):
			cls.utilityManagerObj=UtilityManager()
		return cls.utilityManagerObj

	#Function returns enum value for this operation string
	def getEnumValueForUtilString(self,utilStringInRule):
		return self.ruleStringUtilMap[utilStringInRule]

	#utilKey identifying operation to be performed;args contain other parameters required for performing the operation
	#in case of sorting args identifies keys to perform sort on along with sort order
	#dataList contains data to run utility on
	def run(self,utilKey,dataList,args=None):		
		utilClassKey=self.getClassKeyForOperation(utilKey)
		utilClassObj=self.getObjectForKey(utilClassKey)
		return utilClassObj.run(utilKey,dataList,args)
		
