class DataUtils:
	@classmethod
	def getUniqueKey(cls,keyList):
		keyString=''
		for key in keyList:
			keyString=str(keyString).lower()+str(key)+'#'
		return keyString
	
	@classmethod
	def getKeySet(cls,keyString):
		keyList=keyString.split('#')
		return keyList			
