from enum import Enum
from BaseUtils import BaseUtils
class AssignmentUtils(BaseUtils):
	def __init__(self):
		pass

	class UtilKey(Enum):
		ASSIGN='ASSIGN'

	#Need 3 things: leadId,agentId,groupId
	def assign(self,dataList,keysTupleList):
		pass	

	def run(self,utilKey,dataList,args=None):
		if utilKey == AssignmentUtils.UtilKey.ASSIGN:
			pass
			
