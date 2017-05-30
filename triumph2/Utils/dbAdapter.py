import pyodbc

class dbAdapter:
	TAG='dbAdapter'
	def __init__(self,dbType):
		self.dbType=dbType

	def fetchData(self,queryString):
		if self.dbType == 'REPLICASQL':
			conn=pyodbc.connect('DSN=MSSQL;UID=PBLive;PWD=PB123Live')
			cursor=conn.cursor()
			from Utils.Log import Log
			#Log.v(dbAdapter.TAG,'Query to be fetched is '+queryString)	
			try:
				results=cursor.execute(queryString)				
			except:
				Log.e(dbAdapter.TAG,'Fetch failed '+str(queryString))
			columns=[column[0] for column in cursor.description]
			resultList=[]
			index=0
			for result in results:
				resultList.append(zip(columns,result))
				record=resultList[index]
				for attribute in record:
					pass
					#print str(attribute[0])+' value is '+str(attribute[1])
				index=index+1
			#print 'List of attributes of results fetched are : '+str(resultList)
			return resultList
		elif self.dbType == 'PRODSQL':
			conn=pyodbc.connect('DSN=MSSQLPROD;UID=PBLive;PWD=PB123Live')
			cursor=conn.cursor()	
			results=cursor.execute(queryString)				
			columns=[column[0] for column in cursor.description]
			resultList=[]
			index=0
			for result in results:
				resultList.append(zip(columns,result))
				record=resultList[index]
				for attribute in record:
					pass
					#print str(attribute[0])+' value is '+str(attribute[1])
				index=index+1
			#print 'List of attributes of results fetched are : '+str(resultList)
			return resultList
		

	
