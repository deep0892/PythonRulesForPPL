#General Utils include 
#Sorting and Searching
#Aggregate Functions : Sum,Count,Avg 
from enum import Enum
from operator import attrgetter
from BaseUtils import BaseUtils

"""
def l1count(values):
	return values['L1Count']
"""

class GeneralUtils(BaseUtils):
	TAG='GeneralUtils'
	def __init__(self):
		pass

	#Class to map sort order for sorting utility
	class SortOrder(Enum):
		ASC='ASC'
		DESC='DESC'
	
	#Class to map utilities against keys 
	class UtilKey(Enum):
		SORT='SORT'

	
	#dataList is the list of objects containing the data to be sorted based on keys provided along as args
	#keysTuple is a list of tuples containing key and sort order
	def sort(self,dataList,keysTupleList):		
		from Utils.Log import Log
		for tupleKey,tupleOrder in keysTupleList:
			#Log.d(GeneralUtils.TAG,'tuple order is '+str(tupleOrder))
			if tupleOrder == GeneralUtils.SortOrder.ASC:
				dataList.sort(key=lambda x:(x[tupleKey]),reverse=False)
				#sortedList= sorted(dataList.values(),key=l1count,reverse=False)
			else:
				dataList.sort(key=lambda x:(x[tupleKey]),reverse=True)
				#sortedList= sorted(dataList.values(),key=l1count,reverse=True)			
		return dataList

	#args:represents List of arguments for utilKey utility to be run on dataList data
	def run(self,utilKey,dataList,args=None):
		if utilKey == GeneralUtils.UtilKey.SORT:
			return self.sort(dataList,args)	
		

