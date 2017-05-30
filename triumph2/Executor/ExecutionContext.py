"""
Filter out features from a json workflow,find out sequence of its statements
This class object gets created once WorkFlow manager is able to retrieve a workflow
"""

from Generator.models import * 
 
#
class ExecutionContext:
	TAG='ExecutionContext'
	def __init__(self,workflowName,bu,version,developer):
		from Utils.Log import Log
		self.workflowName=workflowName
		self.bu=bu
		self.version=version
		self.developer=developer
		self.featureList=[]
		self.workflow=self.getWorkflowObj(self.workflowName)
		
	#Returns Workflow object from Mongo 	
	def getWorkflowObj(self,workflowNameArg):
		workflow=None
		workflows=Workflow.objects(workflowName=workflowNameArg,bu=self.bu,version=self.version,developer=self.developer)
		for workflow in workflows:
			break
		return workflow
			
	def prepareDB(self):
		import json
		from Executor.models import ActorData
		#Data structures to save data for an execution context
		self.currentAgentsData=ActorData(self.workflowName,self.bu,self.version,self.developer)
		self.currentLeadsData=ActorData(self.workflowName,self.bu,self.version,self.developer)
		

	def saveLeadDataToDB(self,leadDataDict):
		pass			 	

	#Finds out all features that need to be fetched by parsing through workflow and subworkflow objects
	#There are two ways a subWorkflow can be present either as an operation or as an operand
	#As an operand scenario not covered
	def populateFeatureListObj(self,workflow):
		from Utils.Log import Log
		from Utils.TriumphKey import TriumphKey
		if workflow is not None:
			for rule in workflow.rules:
				for operand in rule.operands:
					if operand.opType == TriumphKey.OperandType.FEATURE:
						self.featureList.append(operand.opTag)
					elif operand.opType == TriumphKey.OperandType.OPERATION:
						subWorkflow=self.getWorkflowObj(operand.opTag)
						self.populateFeatureListObj(subWorkflow)				
	
	#Fetch allocation feature values for arguments in inputTuple
	def fetchAllocationFeatureValues(self,featureName,inputTuple):
		from Utils.TriumphKey import TriumphKey
		inputProperties={}
		inputProperties[TriumphKey.FeatureFetchProperty.dataType]=TriumphKey.FeatureType.ALLOCATION
		inputProperties[TriumphKey.FeatureFetchProperty.data]=inputTuple
		from FeatureExec import FeatureExec
		featureExec=FeatureExec()		
		featureValue=featureExec.fetchFeatureValue(featureName,inputProperties)
		return featureValue
		
	#Fetch value of all features of LEAD type and store them in execution context
	def fetchFeatureValueForLeads(self,leadsData,agentsData):
		from FeatureExec import FeatureExec
		from Utils.Log import Log
		from Utils.TriumphKey import TriumphKey
        	featureExec=FeatureExec()
		self.currentLeadsData.actorDataDict={}
		leadsList=[]
		if leadsData is not None:
                        for leadIdKey in leadsData.keys():
                                leadsList.append(leadIdKey)
				self.currentLeadsData.actorDataDict[leadIdKey]=leadsData[leadIdKey]

		self.currentAgentsData.actorDataDict=agentsData
                inputProperties={}
                inputProperties[TriumphKey.FeatureFetchProperty.dataType]=TriumphKey.FeatureType.LEAD
                inputProperties[TriumphKey.FeatureFetchProperty.inputDataField]=TriumphKey.LeadInputDataField.leadId
                inputProperties[TriumphKey.FeatureFetchProperty.data]=leadsList
		from FeatureManager.FeatureStore import FeatureStore
		fs=FeatureStore()
		featureFoundOut=[]
		Log.d(ExecutionContext.TAG, 'List of all features from workflow to be fetched are '+str(self.featureList))
		for feature in self.featureList:
			featureType=fs.getFeatureType(feature)
			if featureType == TriumphKey.FeatureType.AGENT or featureType == TriumphKey.FeatureType.ALLOCATION:
				continue	
			#To avoid fetching same feature multiple times
			if feature not in featureFoundOut:
				featureFoundOut.append(feature)
			else:
				#Feature has already been found out for each lead
				continue
	
			#Now beginning to fetch feature data	
	                featureValues4AllLeads=featureExec.fetchFeatureValue(feature,inputProperties)
			#In case sql query failed and no data was fetched
			if featureValues4AllLeads is None:
				continue

			#Processing data lead by lead as data has been fetched for multiple leads
			for featureValuesPerLead in featureValues4AllLeads:				
				leadPropDict={}
				#Saving data for all attributes: first argument being attribute name and second being value
				for featureValTuple in featureValuesPerLead:
					if featureValTuple[0]!='leadId':
						leadPropDict[str(featureValTuple[0])]=featureValTuple[1]			
					else:
						leadId=featureValTuple[1]
				
				#In case of data being already present for a lead append new attributes to existing dictionaries
				#else create a dictionary entry for this lead in currentLeadsData
				#Skipping putting an entry for an attribute of a lead if its already present
				if self.currentLeadsData.actorDataDict.has_key(leadId) is True:
					prevDataTemp=self.currentLeadsData.actorDataDict[leadId]
					for key in leadPropDict.keys():
						if prevDataTemp.has_key(key) is False:
							prevDataTemp[key]=leadPropDict[key]
						else:
							Log.d(ExecutionContext.TAG,'Entry already present in dictionary for this lead so skipping'+str(key))
					self.currentLeadsData.actorDataDict[leadId]=prevDataTemp
				else:
					self.currentLeadsData.actorDataDict[leadId]=leadPropDict
		#print 'fetchFeatureValue for Leads:----------------------'
		#print 'Current leads data is '+str(self.currentLeadsData.actorDataDict)
		#print 'Current agents data is '+str(self.currentAgentsData.actorDataDict)
