from models import *

class WorkflowManager:
	TAG='WorkflowManager'
	def __init__(self):
		pass

	def createUtilObj(self,util):
		from Generator.models import *
		from Utils.Log import Log
		preUtilsJSONObj=util
		utilKeyJSONList=preUtilsJSONObj['key']
		dataOperandJSON=preUtilsJSONObj['data']
		
		keyList=[]
		for keyJSONObject in utilKeyJSONList:
			key=UtilKey(tag=keyJSONObject['tag'],order=keyJSONObject['order'])
			key.save()
			keyList.append(key)

		#Util operand to run utility on
		operand=Operand(opType=dataOperandJSON['type'],opTag=dataOperandJSON['tag'])
		operand.save()
		dataOperandList=[]
		dataOperandList.append(operand)
		ruleUtilObj=Util(util=preUtilsJSONObj['util'],data=dataOperandList,keys=keyList)				
		ruleUtilObj.save()
		return ruleUtilObj	
	
	def createRuleObj(self,rule):
		operandsDictList=rule['operands']
		from Utils.Log import Log
		operandList=[]
		operandIndex=0
		if rule.has_key('preutil') is False:
			ruleUtilObj=None
		elif rule['preutil']=='None':
			ruleUtilObj=None
		else:
			ruleUtilObj=self.createUtilObj(rule['preutil'])
						
		ruleUtilObjList=[ruleUtilObj]
		for operandDict in operandsDictList:
			#ToDo: Support for a feature containing other features as operands
			if operandDict['type']=='operation':
				ruleObj=[]
				#using magic value of 0 because in case of operation being present in operand;first element in operand list needs to be taken as a rule
				ruleObj.append(self.createRuleObj(operandDict['subRule'][0]))
				operandList.append(Operand(opType=operandDict['type'],subRule=ruleObj))
				#elif operandDict['type']=='feature':
				#ruleObj.			
			else:							
				operandList.append(Operand(opType=operandDict['type'],opTag=operandDict['tag']))
			operandList[operandIndex].save()
			operandIndex=operandIndex+1

		if rule.has_key('nextRuleIndex') is True:
			nRIndex=rule['nextRuleIndex']
			if nRIndex is None or nRIndex == 'None':		
				nRIndex=-1
		else:
			nRIndex=-1

		if rule.has_key('trueRuleIndex') is True:
			trueRIndex=rule['trueRuleIndex']
			if trueRIndex is None or trueRIndex == 'None':
				trueRIndex=-1
		else:
			trueRIndex=-1

		if rule.has_key('falseRuleIndex') is True:
			falseRIndex=rule['falseRuleIndex']
			if falseRIndex is None or falseRIndex == 'None':
				falseRIndex=-1
		else:
			falseRIndex=-1
		"""
		print rule['operator']
		for operand in operandList:
			print str(operand.opTag)+str(operand.opType)
		#print operandList
		print rule['index']
		print rule['depth']
		print trueRIndex
		print falseRIndex
		print 'nRIndex '+str(nRIndex)
		"""		

		newRule=Rule(operator=rule['operator'],operands=operandList,index=rule['index'],depth=rule['depth'],nextRuleIndex=nRIndex,trueRuleIndex=trueRIndex,falseRuleIndex=falseRIndex,preUtils=ruleUtilObjList)
		#print 'True Rule Index and False Rule Index values are '+str(trueRIndex)+str(falseRIndex)
		newRule.save()
        	return newRule
		
	
	def addWorkflow(self,jsonFileLoc):
		import json
		from Generator.models import *
		with open(jsonFileLoc) as data_file:
			data=json.load(data_file)			
	        rules=data['rules']
		rulesList=[]
		for rule in rules:
			newRule=self.createRuleObj(rule)
			rulesList.append(newRule)				
		Workflow(workflowName=data['workflowName'],bu=data['bu'],version=data['version'],developer=data['developer'],rules=rulesList).save()

	def getWorkflow(self,workflowNameArg,buArg,versionArg,developerArg):
		workflow=None
		for workflow in Workflow.objects(workflowName=workflowNameArg,bu=buArg,version=versionArg,developer=developerArg):
			break
		return workflow

	def cleanAllWorkflows(self,workflowNameArg,buArg,versionArg,developerArg):
		Workflow.objects(workflowName=workflowNameArg,bu=buArg,version=versionArg,developer=developerArg).delete()		
		Workflow.objects().delete()


	 
