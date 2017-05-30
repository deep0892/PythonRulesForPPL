from django.test import TestCase

# Create your tests here.

class HomeTest(TestCase):
        def test_add_feature_to_featurelist(self):
                from FeatureStore import FeatureStore
                fs=FeatureStore()
                fs.saveFeatureQuery('hasRevenue','select leadId,model_score from optimus.opt.leaddetails ld with(nolock) ','LEAD')
                fs.saveFeatureQuery('isSameCustomer','select leadId,model_score from optimus.opt.leaddetails ld with(nolock) ','LEAD')
		#fs.saveFeatureQuery('isAskTerry','select leadId,model_score from optimus.opt.leaddetails ld with(nolock)','LEAD')
                print 'getFeature to be called ---------------------------'
                print fs.getFeatureQS('isSameCustomer')
                from Executor.FeatureExec import FeatureExec
                featureExec=FeatureExec()
                inputProperties={}
                inputProperties['dataType']='LEAD'
                #leadId,mobileNo
                inputProperties['inputDataField']='leadId'
                inputProperties['data']=['28691527']
                featureExec.fetchFeatureValue('isSameCustomer',inputProperties)

