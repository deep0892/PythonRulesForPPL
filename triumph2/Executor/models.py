from django.db import models
from mongoengine import *

class ActorData:
	def __init__(self,workflowNameArg,buArg,versionArg,developerArg):
		self.actorDataDict={}
		self.workflowName=workflowNameArg
	        self.bu=buArg
		self.version=versionArg
		self.developer=developerArg


"""
class CurrentAgentsData(Document):
	agents=ListField()
	workflowName=StringField(max_length=50,required=True)
        bu=StringField(max_length=50,required=True)
	version=IntField()
	developer=StringField(max_length=50,required=True)

class AgentData(Document):
	agentId=StringField(max_length=50,required=True)
	properties=DictField()	

class CurrentLeadsData(Document):
	leads=ListField()
	workflowName=StringField(max_length=50,required=True)
        bu=StringField(max_length=50,required=True)
	version=IntField()
	developer=StringField(max_length=50,required=True)

class LeadData(Document):
	leadId=StringField(max_length=50,required=True)
	properties=DictField()
"""
	
