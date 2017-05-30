from abc import ABCMeta,abstractmethod

class BaseUtils:
	__metaclass__=ABCMeta

	#Finds function mapping a string and executes it 
	#Checks integrity of operands for each function call	
	@abstractmethod
	def run(self,utilKey,dataList,args=None):
		pass

