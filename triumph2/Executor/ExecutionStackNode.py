#
#Maintains meta data for stack
#
class ExecutionStackNode:
	from enum import Enum
	TAG='ExecutionStackNode'
	class STACKNODETYPE(Enum):
		DATALOOP=1
		COUNTERLOOP=2

	#Support for counter loop to be added later
	def __init__(self,workflowName,depth,nextRuleIndex,stackType,dataList=None):
		from Utils.Log import Log
		self.depth=depth
		self.workflowName=workflowName
		#Index for containing the beginning rule of a block statement
		self.nextRuleIndex=nextRuleIndex
		#Current index in iteration of the loop
		self.currentIndex=0
		self.stackType=stackType
		#Gets set only in case of Data loop
		self.dataList=dataList	
		self.currentIterationData=self.dataList[self.currentIndex]
		self.assigned=False
	
	#pops out of loop with false return value if final condition met;returns False if final condition is not met
	def iterate(self):
		from Utils.Log import Log
		if self.stackType == ExecutionStackNode.STACKNODETYPE.DATALOOP:
			self.dataList[self.currentIndex]=self.currentIterationData
			self.currentIndex=self.currentIndex +1
			"""for data in self.dataList:
				Log.d(ExecutionStackNode.TAG,' L1Count is '+str(data['L1Count'])+'#'+str(data['L2Count']))"""
			if self.currentIndex < len(self.dataList):
				self.currentIterationData=self.dataList[self.currentIndex]
				return True
			else:
				return False			
		elif self.stackType == ExecutionStackNode.STACKNODETYPE.COUNTERLOOP:
			pass
