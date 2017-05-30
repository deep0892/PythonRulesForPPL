from django.test import TestCase

# Create your tests here.
# Tasks:
# ------
# Build script in python
# ----------------------
# Read json workflow 
# 
# Create SQL queries from relationPaths in tables
# 
class HomeTest(TestCase):
	def test_add_feature_to_featurelist(self):
		print 'Test add feature to featureList'
                from FeatureManager.FeatureStore import FeatureStore
                fs=FeatureStore()
		# Rules for a query
		# LEAD query strings must have optimus.ld.leaddetails and should be shortformed ld
		# Select query must have leadId output parameter... Case to be taken care of
                #fs.saveFeatureQuery(['isModelScoreL1','modelScoreL1'],'select ld.leadId as leadId,leadId as isModelScoreL1,model_score as modelScoreL1 from optimus.opt.leaddetails ld with(nolock) ','LEAD')
		fs.saveFeatureQuery(['isSameCustomer','sameCustomerScore'],'select ld.leadId as leadId,leadId as isSameCustomer,model_score as sameCustomerScore from optimus.opt.leaddetails ld with(nolock) ','LEAD')
                fs.saveFeatureQuery(['isAskTerry','askTerryScore'],'select ld.leadId as leadId,leadId as isAskTerry,model_score as askTerryScore from optimus.opt.leaddetails ld with(nolock) ','LEAD')
		#fs.saveFeatureQuery(['leadsCount','leadsPPL','Grade','GroupId','GroupName','DailyLimit','BucketSize','MaxLeadsPPLCount','L1Count','L2Count','L3Count'],'None','AGENT')
		#fs.saveFeatureQuery(['isL1','isL2','isL3'],'None','LEAD')
		fs.saveFeatureQuery(['APercent'],'SELECT Coeff FROM REPLPBCROMA.MTX.Ref_AttributeDetails with(nolock) WHERE ProductId=7 AND attr2 = %d  and Attr1 = %d','ALLOCATION')	
		#fs.saveFeatureQuery(['isSameCustomer'],'SELECT case when count(LD.LeadID)>0 then True else False end as isSameCustomer FROM  REPLPBCROMA.CRM.Leaddetails LD WITH(NOLOCK) INNER JOIN REPLPBCROMA.CRM.LeadAssignDetails LAD WITH(NOLOCK) ON LD.LeadID=LAD.LeadID AND LD.ProductID in (1,117) AND  (LD.IsActive=1 OR LD.IsActive  IS NULL) AND   LAD.IsLastAssigned=1 AND  (LAD.AssignedToUserID IS NOT NULL OR LAD.AssignedToUserID<>0) INNER JOIN REPLPBCROMA.CRM.UserDetails UD WITH (NOLOCK) ON UD.UserID=LAD.AssignedToUserID AND UD.IsActive=1 INNER JOIN REPLPBCROMA.CRM.UserGroupRoleMapNew UGRMN WITH (NOLOCK) ON UGRMN.UserID=UD.UserID AND UGRMN.AutoAllocation=1 INNER JOIN REPLPBCROMA.CRM.RoleSuperMaster RSM WITH (NOLOCK) ON UGRMN.RoleSuperId=RSM.RoleSuperId AND RSM.RoleCategoryID =2 AND RSM.RoleId=13 INNER JOIN REPLPBCROMA.CRM.PermissionDetails PD WITH (NOLOCK) ON UGRMN.UserId=PD.UserId AND PD.ProcessId  =2 INNER JOIN REPLPBCROMA.CRM.ProductGroupMapping PGM WITH(NOLOCK) ON PGM.GroupId=UGRMN.GroupId AND PGM.ProductId in (1,117) INNER JOIN REPLPBCROMA.CRM.UserGroupMaster UGM WITH(NOLOCK) ON PGM.GroupId=UGM.UserGroupID and (UGM.IsBMSGroup=0 OR UGM.IsBMSGroup IS NULL) LEFT JOIN REPLPBCROMA.crm.BookingDetails BD WITH(NOLOCK) ON LD.LeadID=BD.LeadID WHERE ( BD.paymentSTATUS IN(5001,3001,1001,4001,6001,0,1)  OR BD.paymentSTATUS IS NULL  OR BD.paymentSTATUS  =\'\')','LEAD')
		#fs.saveFeatureQuery(['sameCustomerUserId','sameCustomerLeadId','sameCustomerAgentGrade','sameCustomerEmployeeId'],'SELECT count(LD.LeadID), UD.UserID as sameCustomerUserId ,LD.LeadID as sameCustomerLeadId,UD.Grade as sameCustomerAgentGrade,ud.EmployeeId as sameCustomerEmployeeId FROM  REPLPBCROMA.CRM.Leaddetails LD WITH(NOLOCK) INNER JOIN REPLPBCROMA.CRM.LeadAssignDetails LAD WITH(NOLOCK) ON LD.LeadID=LAD.LeadID AND LD.ProductID in (1,117) AND  (LD.IsActive=1 OR LD.IsActive  IS NULL) AND   LAD.IsLastAssigned=1 AND  (LAD.AssignedToUserID IS NOT NULL OR LAD.AssignedToUserID<>0) INNER JOIN REPLPBCROMA.CRM.UserDetails UD WITH (NOLOCK) ON UD.UserID=LAD.AssignedToUserID AND UD.IsActive=1 INNER JOIN REPLPBCROMA.CRM.UserGroupRoleMapNew UGRMN WITH (NOLOCK) ON UGRMN.UserID=UD.UserID AND UGRMN.AutoAllocation=1 INNER JOIN REPLPBCROMA.CRM.RoleSuperMaster RSM WITH (NOLOCK) ON UGRMN.RoleSuperId=RSM.RoleSuperId AND RSM.RoleCategoryID =2 AND RSM.RoleId=13 INNER JOIN REPLPBCROMA.CRM.PermissionDetails PD WITH (NOLOCK) ON UGRMN.UserId=PD.UserId AND PD.ProcessId  =2 INNER JOIN REPLPBCROMA.CRM.ProductGroupMapping PGM WITH(NOLOCK) ON PGM.GroupId=UGRMN.GroupId AND PGM.ProductId in (1,117) INNER JOIN REPLPBCROMA.CRM.UserGroupMaster UGM WITH(NOLOCK) ON PGM.GroupId=UGM.UserGroupID and (UGM.IsBMSGroup=0 OR UGM.IsBMSGroup IS NULL) LEFT JOIN REPLPBCROMA.crm.BookingDetails BD WITH(NOLOCK) ON LD.LeadID=BD.LeadID WHERE ( BD.paymentSTATUS IN(5001,3001,1001,4001,6001,0,1)  OR BD.paymentSTATUS IS NULL  OR BD.paymentSTATUS  =\'\')','LEAD')

		#Need to check this for same product as well

		#fs.saveFeatureQuery(['isAskTerryLead'],'select case when ld.utm_term =\'askterry\' then True else False end from replpbcroma.crm.leaddetails ld with(nolock)','LEAD')
		#fs.saveFeatureQuery(['isMobileAppLead'],'','LEAD')
		#fs.saveFeatureQuery(['isL1'],'','LEAD')
		#fs.saveFeatureQuery(['isL2'],'','LEAD')
		#fs.saveFeatureQuery(['isL3'],'','LEAD')
		
		#Agent SubRules to be computed from agent data stored locally instead of sql server
		#isA1AgentAvailable
		#isA2AgentAvailable
		#isA3AgentAvailable
		
		#subRules
		#assignToMobileAppAgent
		#assignToAskTerryAgent
		#assignToSameAgent
		#assignToA1Agent
		#assignToA2Agent
		#assignToA3Agent
		#leaveUnAssigned

		#assignLead is a default rule which saves a lead and agent mapping to db

	def test_find_all_features_in_workflow(self):
		from mongoengine import connect
                MONGO_DATABASE_NAME='testdb'
                MONGO_HOST='127.0.0.1'
                MONGO_PORT=27017
                connect('testdb',host=MONGO_HOST,port=MONGO_PORT)
		"""
		from Executor.ExecutionContext import ExecutionContext 
		executionContext=ExecutionContext('testsqlquery','tech',0,'sanket')
                executionContext.prepareDB()
                executionContext.populateFeatureListObj()
		leadsList=['28855508']
		executionContext.fetchFeatureValueForLeads(leadsList,None)
		"""

	def test_making_allocation(self):
		from AllocationService import AllocationService
		from Allocation import Allocation
		AllocationService.initialize()
		allocationObj=Allocation()	
		allocationObj.createExecutionContext()	
		allocationObj.allocate()
