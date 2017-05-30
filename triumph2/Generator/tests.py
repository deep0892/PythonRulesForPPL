from django.test import TestCase
import json
import glob,os
#from scriptRunner.Data import QueryBuilder 

# Create your tests here.
class HomeTest(TestCase):
	def test_save_json_data_to_mongo(self):		
		from mongoengine import connect
		MONGO_DATABASE_NAME='testdb'
		MONGO_HOST='127.0.0.1'
		MONGO_PORT=27017
	        connect('testdb',host=MONGO_HOST,port=MONGO_PORT)
		from Generator.WorkflowManager import *		
		wfManager=WorkflowManager()
		wfManager.cleanAllWorkflows('termAllocation','tech',0,'sanket')
		parentPath='Generator/Workflows/'
		cwd=os.getcwd()
		os.chdir(parentPath)
		for file in glob.glob("*.json"):
			#print (cwd+'/'+parentPath+str(file))
			#print cwd+'/'+parentPath+str(file)
			wfManager.addWorkflow(cwd+'/'+parentPath+str(file))
			
		#print str(data)
		#jsonData=json.loads(str(data))					
		#print data['developer']
		#print data

	def test_add_feature_to_featurelist(self):
		from FeatureManager.FeatureStore import FeatureStore
		#qb=QueryBuilder()
		#qb.saveFeatureQuery('hasRevenue','select count(*) from ','LEAD')
		#print 'testing adding of feature to featureList'
