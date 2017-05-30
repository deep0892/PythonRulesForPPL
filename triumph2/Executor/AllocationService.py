
class AllocationService:
	@classmethod
	def initialize(cls):		
		cls.workflowManager=None
		cls.featureStorePath='/home/policy/Sanket/02Sources/triumphAttempts/triumph2/triumph2/Utils/QueryStrings1.json'

	@classmethod
	def getFeatureStorePath(cls):
		return cls.featureStorePath

	@classmethod
	def getWorkflowManager(cls):
		from Generator.WorkflowManager import WorkflowManager 
		if cls.workflowManager is None:
			cls.workflowManager=WorkflowManager()
			return cls.workflowManager
		else:
			return cls.workflowManager



