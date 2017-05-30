from Executor.ExecutionStackNode import ExecutionStackNode

class Allocation:
	TAG='Allocation'
	def __init__(self):
		from Utils.Cache import Cache
		self.leadsList=[]
		self.agentsList=[]
		self.mCache=Cache()

	def fetchLeadsAndAgentsData(self):
		from Utils.Log import Log
		import sys
		this_function_name = sys._getframe().f_code.co_name	
		Log.log(Allocation.TAG,this_function_name)
		from Executor.InputDataExtracter import InputDataExtracter 
		inputDataExtracter=InputDataExtracter()
		inputDataExtracter.setInputLeadsQuery(None)
		inputDataExtracter.setInputAgentsQuery(None)
		self.inputLeadsData=inputDataExtracter.fetchInputLeads()
		self.inputAgentsData=inputDataExtracter.fetchInputAgents()
		self.leadAssignmentData=[] # Contains pair of lead against Agent
		
		if self.inputLeadsData is not None:
			for leadIdKey in self.inputLeadsData.keys():
				self.leadsList.append(leadIdKey)
		else:
			Log.log(Allocation.TAG,'Input leads data is None')
		if self.inputAgentsData is not None:
			for key in self.inputAgentsData.keys():
				pass
				
	def createExecutionContext(self):			
		from Utils.Log import Log
		from mongoengine import connect
                MONGO_DATABASE_NAME='testdb'
                MONGO_HOST='127.0.0.1'
                MONGO_PORT=27017
                connect('testdb',host=MONGO_HOST,port=MONGO_PORT)
		self.workflowName='termAllocation'
		bu='tech'
		version=0
		developer='sanket'		
                from Executor.ExecutionContext import ExecutionContext
                self.executionContext=ExecutionContext(self.workflowName,bu,version,developer)
                self.executionContext.prepareDB()
                self.executionContext.populateFeatureListObj(self.executionContext.workflow)
		Log.log(Allocation.TAG,'Feature list is '+str(self.executionContext.featureList))
		self.fetchLeadsAndAgentsData()
		self.executionContext.fetchFeatureValueForLeads(self.inputLeadsData,self.inputAgentsData)

	def prepareOperand(self,operand,inputLeadDataDict,executionStack):
		from Utils.Log import Log
		from Utils.TriumphKey import TriumphKey
		if len(executionStack) > 0:
			currentAgentDataDict=executionStack[-1].currentIterationData
		else:
			currentAgentDataDict=None
		if operand.opType == TriumphKey.OperandType.LITERAL:
			return operand.opTag
		elif operand.opType == TriumphKey.OperandType.FEATURE:
			if inputLeadDataDict.has_key(operand.opTag) is True:
				return inputLeadDataDict[operand.opTag]					
			elif currentAgentDataDict is not None:
				#check for data in current execution stack
				Log.d(Allocation.TAG,currentAgentDataDict)
				if currentAgentDataDict.has_key(operand.opTag) is True:
					return currentAgentDataDict[operand.opTag]
				return None
			else:
				#TODO: Ideally allocation type of feature should be handled here
				Log.log(Allocation.TAG,'Could not find data for this feature'+str(operand.opTag))
				return None
		elif operand.opType == TriumphKey.OperandType.OPERATION:
			subRule=operand.subRule[0]
			subRuleName=subRule.operands[0].opTag
			subWorkflow=self.workflowManager.getWorkflow(subRuleName,'tech',0,'sanket')
			if subWorkflow is not None:
				return self.runWorkflow(subWorkflow,inputLeadDataDict,executionStack)
		elif operand.opType == TriumphKey.OperandType.VAR:
			if operand.opTag=='agents':
				agentDataList=[]
				for key,agentData in self.inputAgentsData.iteritems():
					agentDataList.append(agentData)
				return agentDataList

	def findNextIndex(self,result,curRule):
		from Utils.Log import Log
		curIndex=0
		if result is True:
			if curRule.trueRuleIndex == 'None':
				curIndex=None
			curIndex=curRule.trueRuleIndex
		elif result is False:
			if curRule.falseRuleIndex == 'None':
				curIndex=None
			curIndex=curRule.falseRuleIndex
		else:
			if curRule.nextRuleIndex == 'None':
				curIndex=None
			curIndex=curRule.nextRuleIndex					
		return curIndex	
	
	#executes logical,arithematic operations::: Cases:
	#feature:fetch from sql server ALLOCATION feature value and return
	#loop: Create an executionStackNode which contains data for the loop
	#subRule: runWorkflow and return result to caller of this operation
	#else: Run operation command 
	def runOperation(self,workflowName,curRule,operandList,executionStack,inputLeadDataDict):
		#Process Operator on gathered list of operands
		from Utils.TriumphKey import TriumphKey
		from Utils.Log import Log
		result=0
		if curRule.operator == TriumphKey.Operator.FEATURE:
			from FeatureManager.FeatureStore import FeatureStore
			fs=FeatureStore()
			allocationFeature=curRule.operands[0].opTag
			allocOperandList=operandList[1:]
			allocOperandTuple=tuple(operandList[1:])
			featureType=fs.getFeatureType(allocationFeature)	
			if featureType==TriumphKey.FeatureType.ALLOCATION:				
				if self.mCache.getData(allocationFeature,allocOperandList) is None:
					result=self.executionContext.fetchAllocationFeatureValues(allocationFeature,allocOperandTuple)
					result=result[0][0][1]
					self.mCache.saveData(allocationFeature,allocOperandList,result)
				else:
					result=self.mCache.getData(allocationFeature,allocOperandList)
				if result is not None:
					Log.d(Allocation.TAG,'Found an allocation feature name'+str(allocationFeature))
				#result=result[0]
		elif curRule.operator == TriumphKey.Operator.LOOP:
			dataList=operandList[0]
			executionStack.append(ExecutionStackNode(workflowName,curRule.depth,curRule.nextRuleIndex,ExecutionStackNode.STACKNODETYPE.DATALOOP,dataList))								
		elif curRule.operator == TriumphKey.Operator.SUBRULE:
			from AllocationService import AllocationService
			self.workflowManager=AllocationService.getWorkflowManager()
			if operandList[0] == 'assignA1' or operandList[0] == 'assignA2' or operandList[0] =='assignA3':
				executionStack[-1].assigned=True
			newWorkflow=self.workflowManager.getWorkflow(operandList[0],'tech',0,'sanket')				
			if newWorkflow is not None:
				result=self.runWorkflow(newWorkflow,inputLeadDataDict,executionStack)	
		else:					
			from Executor.Operation import Operation
			operandListTuple=tuple(operandList)
			operation=Operation(curRule.operator,operandListTuple)	
			result=operation.operate()
		return result
	
	def runWorkflow(self,workflow,inputLeadDataDict,executionStackArg):
		from Utils.Log import Log
		#rulesDictionary is created per Workflow		
		rulesDictionary={}
		for rule in workflow.rules:
			rulesDictionary[rule.index]=rule
		curIndex=0
		curRule=rulesDictionary[curIndex]
		result=0
		executionStack=executionStackArg
		while curRule is not None:						
			result=0
			operandList=[]
			#Prepare all operands and store their values in operandList;allocation features currently not handled here
			for operand in curRule.operands:				
				operandList.append(self.prepareOperand(operand,inputLeadDataDict,executionStack))
				"""for operandItem in operandList:
					Log.log(Allocation.TAG, 'workflow '+str(workflow.workflowName)+'Operand is '+str(operandItem))"""
			
			if curRule.preUtils is not None:
				preUtils=curRule.preUtils[0]
				if preUtils is not None:
					from Utils.UtilityManager import UtilityManager
					utilityManager=UtilityManager.getUtilityManager()
					agentDataList=[]
					for key,agentData in self.inputAgentsData.iteritems():
						agentDataList.append(agentData)
					from Utils.GeneralUtils import GeneralUtils
					keyOrderTupleList=[]
					for key in preUtils.keys:
						keyOrderTupleList.append((str(key.tag),str(key.order)))
					utilKey=utilityManager.getEnumValueForUtilString(preUtils.util)
				        agentDataList=utilityManager.run(utilKey,agentDataList,keyOrderTupleList)	
					"""for agentData in agentDataList:
						listOfKeyParts=[agentData['UserID'],agentData['EmployeeId'],agentData['Grade'],agentData['GroupId'],agentData['UserGroupName'],agentData['limit'],agentData['BucketSize'],agentData['PPLLimit']]
		                                agentDataKey=DataUtils.getUniqueKey(listOfKeyParts)
						#self.inputAgentsData[agentDataKey]=agentData
					for agentData in agentDataList:
						Log.d(Allocation.TAG,str(agentData['L1Count'])+str(agentData['L2Count']))"""
					operandList[0]=agentDataList
					#Log.log(Allocation.TAG,str(preUtils.util)+str(preUtils.data)+str(preUtils.keys))
			#Run operation on operandList data
			result=self.runOperation(workflow.workflowName,curRule,operandList,executionStack,inputLeadDataDict)	
			#Finding out index of next rule to execute	
			curIndex=self.findNextIndex(result,curRule)
			if curIndex is not None and curIndex != -1:
				curRule=rulesDictionary[curIndex]								

			#Below condition becomes true only when we catch a leaf in rule/subRule for current data
			#Iterate through the loop to process subsequent data
			#Need to check if depth of execution stack matches that of rule that has hit deadend
			#If it does,then iterate to next set of data and set current rule index to first rule in loop statement
			#If not then return result of running workflow to caller workflow
			if curIndex == None or curIndex == -1:				
				if len(executionStack) > 0:
					if executionStack[-1].workflowName != workflow.workflowName:
						return result
				flag=0
				stackNode=executionStack[-1]
				if stackNode.stackType == ExecutionStackNode.STACKNODETYPE.DATALOOP:
					iterationFlag=stackNode.iterate() 
					if iterationFlag == True and stackNode.assigned is False :
						curIndex=stackNode.nextRuleIndex
						curRule=rulesDictionary[curIndex]
						#print stackNode.currentIterationData
					else:
						executionStack.pop()
						flag=1
						return 							
				else:
					executionStack.pop()
					flag=1
					return
				if flag == 1:
					return
						
	def allocate(self):
		from Utils.Log import Log
		from AllocationService import AllocationService
		from Operation import Operation
		# Save rules in a dictionary with key being the index
		#Log.log(Allocation.TAG, 'Input leads data is '+str(self.inputLeadsData))
		for key,value in self.inputLeadsData.iteritems():
			Log.log(Allocation.TAG,'Running loop for '+str(key))
			self.workflowManager=AllocationService.getWorkflowManager()
		 	workflow=self.workflowManager.getWorkflow(self.workflowName,'tech',0,'sanket')
			self.runWorkflow(workflow,value,[])
