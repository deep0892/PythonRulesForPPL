from django.test import TestCase

# Create your tests here.
class HomeTest(TestCase):
	def test_sort_utility(self):
		from Utils.Log import Log
		from Utils.UtilityManager import UtilityManager
		utilityManager=UtilityManager.getUtilityManager()	  
		from Utils.GeneralUtils import GeneralUtils
		class TestObj:
			def __init__(self,a,b,c):
				self.a=a
				self.b=b
				self.c=c
		TestObjList=[]
		TestObjList.append(TestObj(2,'bhagat singh',45))
		TestObjList.append(TestObj(3,'rajguru',60))
		TestObjList.append(TestObj(5,'chandrashekar',70))
		TestObjList.append(TestObj(5,'netaji',90))
		from Utils.Cache import Cache
		cacheObj=Cache()
		featureParamList=['A','B']
		featureParamValList=[3,5]
		dataDictionary={'c':30,'d':50}
		#cacheObj.saveData('ABC',featureParamList,featureParamValList,dataDictionary)
		#dataDictionary={'c':20,'d':70}
		#cacheObj.saveData('ABC',featureParamList,featureParamValList,dataDictionary)
		#Log.d('HomeTest',str(cacheObj.getData('ABC',featureParamList,featureParamValList)))	
		"""
		for item in TestObjList:
			print str(item.b)+str(item.a)+str(item.c)
		sortedList=utilityManager.run(GeneralUtils.UtilKey.SORT,TestObjList,[('a','ASC'),('c','DESC')])
		for item in sortedList:
			print str(item.b)+str(item.a)+str(item.c)
		"""
