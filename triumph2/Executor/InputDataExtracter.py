#Class to extract set of leads and agents to run algorithm for

class InputDataExtracter:
	TAG='InputDataExtracter'
	def __init__(self):
		self.leadsFetchQuery=None
		self.agentsFetchQuery=None
	
	def setInputLeadsQuery(self,queryString):
		#self.leadsFetchQuery=queryString
		self.leadsFetchQuery='SELECT (case when LGR.LeadGrade = 6 then \'True\' else \'False\' end) AS isL1,(case when LGR.LeadGrade = 7 then \'True\' else \'False\' end) AS isL2,(case when LGR.LeadGrade = 8 then \'True\' else \'False\' end) AS isL3,LD.LeadID,LD.ProductID,LD.MobileNo,LD.Utm_source,ld.CityID,PD.InvestmentTypeID,LD.UTM_Medium,LD.LeadRank,LD.MKTRevenue ,ld.LeadGrade,LD.LeadScore,LeadTypeId,LS.StatusID,LS.SubStatusID,LeadSource,LGR.LeadGrade as ModelGrade,ld.Model_Score FROM (SELECT LD1.LeadID,LD1.ProductID,LD1.MobileNo,LD1.Utm_source,LD1.CityID,LD1.UTM_Medium,LD1.LeadSource,LD1.LeadRank,LD1.MKTRevenue,LD1.LeadGrade,LD1.LeadScore,CASE WHEN LD1.Utm_term = \'askterry\' THEN 3 ELSE 0 END AS LeadTypeId,LD1.Model_Score,LD1.CreatedON FROM   replpbcroma.CRM.LeadDetails LD1 WITH (NOLOCK)INNER JOIN replProductDB.customer.CommPreferences cp with(nolock)  on cp.CustomerID=LD1.CustomerID and cp.ProductID=LD1.ProductID and cp.CommTypeID=3  and cp.IsAssist = 1 WHERE   LD1.ProductID=7 AND LD1.CreatedON BETWEEN \'2015-12-07 00:00:00.000\' AND \'2015-12-15 12:00:00.000\' AND (LD1.IsActive=1 OR LD1.IsActive IS NULL) AND   LeadSource NOT IN (\'Inbound\',\'Referral\',\'Renewal\') AND (LD1.LeadSource <> \'PBMOBILEAPP\' OR LD1.IsAllocable= 1) AND   (LD1.Utm_source NOT LIKE \'%tyroo%\' OR LD1.Utm_source IS NULL) AND   LD1.DOB <> \'NULL\' AND   NOT EXISTS( Select 1 from replpbcroma.CRM.InvalidMobileNumbers InvalidNo WITH(NOLOCK) where InvalidNo.MobileNo = LD1.MobileNo)) LD INNER JOIN  replpbcroma.CRM.ProductDetails PD WITH(NOLOCK) ON LD.LeadID=PD.LeadID INNER JOIN  replProductDB.customer.MobileDetail MD(nolock) ON MD.MobileNo=LD.MobileNo and MD.IsActive=1 INNER JOIN  replProductDB.customer.Registration R(nolock)  ON MD.CustId=R.CustomerId and R.StatusId in(1,2) INNER JOIN  replpbcroma.CRM.LeadStatus LS WITH(NOLOCK) ON LS.LeadID=LD.LeadID AND LS.IsLastStatus=1 and (LS.StatusID in(1,2,3,4,11)) INNER JOIN  replpbcroma.[MTX].[LeadGradeRanges] LGR WITH(NOLOCK) ON LD.ProductId = LGR.ProductId AND LD.Model_Score between LGR.MinModelScore AND LGR.MaxModelScore AND LGR.ProductId=7 LEFT JOIN  replpbcroma.CRM.LeadAssignDetails LAD WITH(NOLOCK) ON LAD.LeadID=LD.LeadID AND IsLastAssigned=1 WHERE   LAD.Assigntogroupid IS NULL AND LAD.Assignedtouserid IS NULL ORDER BY ld.Model_Score desc ,LD.CreatedON DESC'


		
	def setInputAgentsQuery(self,queryString):
		#self.agentsFetchQuery=queryString
		from Utils.dbAdapter import dbAdapter
		dbAdapterObj=dbAdapter('PRODSQL')
		l1MinQS='SELECT MinModelScore from PbCroma.MTX.LeadGradeRanges WITH(NOLOCK) WHERE LeadGrade = 6 AND ProductId=7'
		l1MinDict=dbAdapterObj.fetchData(l1MinQS)
		l1Min=l1MinDict[0][0][1]
		
		l2MinQS='SELECT MinModelScore from PbCroma.MTX.LeadGradeRanges WITH(NOLOCK) WHERE LeadGrade = 7 AND ProductId=7'
		l2MinDict=dbAdapterObj.fetchData(l2MinQS)
		l2Min=l2MinDict[0][0][1]		

		l2MaxQS='SELECT MaxModelScore from PbCroma.MTX.LeadGradeRanges WITH(NOLOCK) WHERE LeadGrade = 7 AND ProductId=7'
		l2MaxDict=dbAdapterObj.fetchData(l2MaxQS)
		l2Max=l2MaxDict[0][0][1]		

		l3MaxQS='SELECT MaxModelScore from PbCroma.MTX.LeadGradeRanges WITH(NOLOCK) WHERE LeadGrade = 8 AND ProductId=7'
		l3MaxDict=dbAdapterObj.fetchData(l3MaxQS)
		l3Max=l3MaxDict[0][0][1]
		self.agentsFetchQuery='SELECT top 100 lad.AssignedToUserID AS UserID,Ld.LeadID,ISNULL(LD.MKTRevenue,0) AS LeadsPPL,UD.EmployeeId,UD.Grade,UGRN.GroupId,G.UserGroupName,ud.limit,ud.BucketSize,UD.PPLLimit ,case WHEN LD.Model_Score >= '+str(l1Min)+' Then 1 ELSE 0 end L1Count,case WHEN LD.Model_Score <'+str(l1Min)+' and LD.Model_Score>='+str(l2Min)+' Then 1 ELSE 0 end L2Count,case WHEN isnull(LD.Model_Score,0) < '+str(l2Min)+' Then 1 ELSE 0 end L3Count FROM replpbcroma.CRM.UserGroupRoleMapNew AS UGRN INNER JOIN replpbcroma.CRM.UserDetails ud WITH(NOLOCK) ON ud.UserID=UGRN.UserId AND ud.IsActive=1 INNER JOIN replpbcroma.CRM.LeadAssignDetails lad WITH (NOLOCK)  ON   lad.AssignedToUserID = UD.UserId AND lad.CreatedOn > GETDATE() -150 AND lad.IsLastAssigned = 1 INNER JOIN replpbcroma.CRM.Leaddetails AS LD WITH (NOLOCK) ON lad.LeadID = LD.LeadID AND (LD.IsActive IS NULL OR LD.IsActive = 1) INNER JOIN replProductDB.customer.MobileDetail MD(nolock) ON MD.MobileNo=LD.MobileNo and MD.IsActive=1 INNER JOIN replproductDB.customer.Registration R(nolock)  ON MD.CustId=R.CustomerId and R.StatusId in(1,2) INNER JOIN replpbcroma.CRM.PermissionDetails PD (NOLOCK) ON UGRN.UserId=PD.UserId  AND PD.ProcessId =2 AND UGRN.RoleSuperId=11 AND UGRN.AutoAllocation=1 INNER JOIN ( SELECT DISTINCT UGM.UserGroupID,UGM.UserGroupName 	   FROM replpbcroma.CRM.UserGroupMaster UGM WITH(NOLOCK) INNER JOIN replpbcroma.CRM.ProductGroupMapping PG (NOLOCK) ON PG.GroupId = ugm.UserGroupID AND (UGM.IsBMSGroup IS NULL OR UGM.IsBMSGroup=0) and pg.ProductId = 1000)G ON G.UserGroupID=UGRN.GroupId INNER JOIN	replpbcroma.CRM.LeadStatus AS ls WITH (NOLOCK) ON ls.LeadID = lad.LeadID AND ls.IsLastStatus = 1 INNER JOIN replpbcroma.CRM.StatusMaster AS sm WITH (NOLOCK) ON sm.StatusId = ls.StatusID and (sm.StatusMode = \'P\' OR sm.StatusMode IS NULL)'

	def fetchInputLeads(self):
		allLeadsDataDict={}
		if self.leadsFetchQuery is not None:
			from Utils.dbAdapter import dbAdapter
			dbAdapter=dbAdapter('REPLICASQL')	
			self.leadsDataList=dbAdapter.fetchData(self.leadsFetchQuery)	
			for leadsData in self.leadsDataList:
				currentLeadData={}
				for element in leadsData:
					if element[0]=='LeadID':
						key=element[1]
					else:
						currentLeadData[element[0]]=element[1]
				allLeadsDataDict[key]=currentLeadData
			return allLeadsDataDict
		else:
			return None
	
	def fetchInputAgents(self):
		if self.agentsFetchQuery is not None:
			from Utils.dbAdapter import dbAdapter
			from Utils.DataUtils import DataUtils
			from Utils.Log import Log
			dbAdapter=dbAdapter('REPLICASQL')	
			self.agentsDataList=dbAdapter.fetchData(self.agentsFetchQuery)			
			self.allAgentsDataDict={}
			for agentData in self.agentsDataList:
				currentAgentData={}
				#Converting complete agent data to dictionary for easy computation
				for element in agentData:
					currentAgentData[element[0]]=element[1]
				if currentAgentData['Grade'] not in (3,4,5):
					continue
				#Segregating parts of a key and generating key to calculate aggregate values for a key
				listOfKeyParts=[currentAgentData['UserID'],currentAgentData['EmployeeId'],currentAgentData['Grade'],currentAgentData['GroupId'],currentAgentData['UserGroupName'],currentAgentData['limit'],currentAgentData['BucketSize'],currentAgentData['PPLLimit']]
				agentDataKey=DataUtils.getUniqueKey(listOfKeyParts)
				#To check if this agent key is already there in processed agents dictionary
				#Log.d(InputDataExtracter.TAG,str(agentDataKey))
				if self.allAgentsDataDict.has_key(agentDataKey) is True:
					#If there was data corresponding to this agent key in all Agents dictionary
					previousAgentsData=self.allAgentsDataDict[agentDataKey]
					previousAgentsData['LeadsCount']=previousAgentsData['LeadsCount']+1
					previousAgentsData['LeadsPPL']=previousAgentsData['LeadsPPL']+currentAgentData['LeadsPPL']
					previousAgentsData['L1Count']=previousAgentsData['L1Count']+currentAgentData['L1Count']
					previousAgentsData['L2Count']=previousAgentsData['L2Count']+currentAgentData['L2Count']
					previousAgentsData['L3Count']=previousAgentsData['L3Count']+currentAgentData['L3Count']
				else:
					#If there was no data previously for this agent in dictionary;previousAgentsData name misleading 
					previousAgentsData={}
					previousAgentsData['LeadsCount']=1
					previousAgentsData['LeadsPPL']=currentAgentData['LeadsPPL']
					previousAgentsData['Grade']=currentAgentData['Grade']
					previousAgentsData['GroupId']=currentAgentData['GroupId']
					previousAgentsData['GroupName']=currentAgentData['UserGroupName']
					previousAgentsData['DailyLimit']=currentAgentData['limit']
					previousAgentsData['BucketSize']=currentAgentData['BucketSize']
					previousAgentsData['MaxLeadsPPLCount']=currentAgentData['PPLLimit']
					previousAgentsData['L1Count']=currentAgentData['L1Count']
					previousAgentsData['L2Count']=currentAgentData['L2Count']
					previousAgentsData['L3Count']=currentAgentData['L3Count']
					previousAgentsData['UserId']=currentAgentData['UserID']
					previousAgentsData['EmployeeId']=currentAgentData['EmployeeId']
								
				self.allAgentsDataDict[agentDataKey]=previousAgentsData
			return self.allAgentsDataDict
		else:
			return None

	
