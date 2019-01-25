#Import Modules
import ast
import sys 
import os
import time
import json
import random
import string
from shutil import copyfile
import datetime

#Add relative PATHs
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Json'))
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'Logs'))

#Import Created Modules
import downloadTweet
import excelExport
import Logger
import Parameters

#Create Reference Code
code = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))

#Create the Logger 
logD = Logger.logs(code)

logD.info('Reference Code: ' + code)

#Get Parameters from the Text File
queryParam = Parameters.getQuery(logD)
queryParam.OAuth()
parameters = queryParam.getParam()

#Variables definition 
companies = parameters[0]
toDate = parameters[1]
fromDate = parameters[2]
consumer_key = parameters[3]
consumer_secret = parameters[4]
devEnv = parameters[5]

#API Connection & Authentication
cnn = downloadTweet.tweets(consumer_key, consumer_secret, logD, devEnv)
cnn.auth()

#Joining companies ID
fromID = 'from:' + companies[0][1]
for i in range(1, len(companies)):
	fromID = fromID + ' OR ' + 'from:' + companies[i][1]

#Sandbox 128 chars & Premium 1024 chars
if len(fromID) > 1024:
	logD.error("Query lenght can't exceed 128 characters") 
	logD.info("Reduce companies to search")
	raise ValueError("Query lenght can't exceed 128 characters")

#Query for the Requested Information 
query =  '{"query":"' + fromID + ' -is:retweet", "fromDate":"' + fromDate[0] + '", "toDate":"' + toDate[0] + '","maxResults":500}' 
#"maxResults":100
#-is:retweet

logD.info('Download Started...')

#First Data Download --> Get Next Code
try:
	data = cnn.download(query)
except: 
	#First Data Download can not Fail --> Next Code
	raise

#Json file PATH
JPATH = os.path.join(os.path.dirname(sys.path[0]),'Json', code + '.json')	

#Open Json Data File
outfile = open(JPATH, 'w')

jsonSave = data[1]
	
#Start Date 
sDate = data[1][-1]['created_at']
	
#Control Variables for Download Errors
run = True	
	
#Download Data	
if len(data) == 4:
	while len(data) == 4 and run:
		try:	
			#Adding Next Parameter	
			query =  '{"query":"' + fromID + ' -is:retweet", "fromDate":"' + fromDate[0] + '", "toDate":"' + toDate[0] + '", "next": "' + data[2] + '","maxResults":500}'
			
			#In case of error, Downloading will Stop
			try:
				data = cnn.download(query)
			except: 
				run = False 

			jsonSave.extend(data[1])
			
			#Limit of RP(Requests per minute)
			time.sleep(2.5)
		except KeyboardInterrupt:
			run = False
		

logD.info('Download Finished...')

#Save Data
json.dump(jsonSave, outfile)

logD.info('Json Data File Created...')

outfile.close()

#Rename JSON with From & To Date
os.rename(os.path.join(os.path.dirname(sys.path[0]),'Json', code + '.json') , os.path.join(os.path.dirname(sys.path[0]),'Json',code + ' - (From ' + sDate.replace(':','.') + ' to ' + data[1][0]['created_at'].replace(':','.') + ').json'))

#PATH Definition
RPATH = os.path.join(os.path.dirname(sys.path[0]),'References', 'References Dictionary.txt')
RBPATH = os.path.join(os.path.dirname(sys.path[0]),'Backup', 'References Dictionary - ' + datetime.datetime.now().strftime("%Y-%m-%d") + ' .txt')
CPATH = os.path.join(os.path.dirname(sys.path[0]),'References', 'Companies Dictionary.txt')
CBPATH = os.path.join(os.path.dirname(sys.path[0]),'Backup', 'Companies Dictionary - ' + datetime.datetime.now().strftime("%Y-%m-%d") + ' .txt')

logD.info('Json File: ' + code + ' - (From ' + sDate.replace(':','.') + ' to ' + data[1][0]['created_at'].replace(':','.') + ').json...')

#Reference
ref = {"Reference":code, "companies":companies, "fromDate":sDate, "toDate":data[1][0]['created_at'], "query": "query: " + fromID + ", fromDate: " + fromDate[0] + ", toDate: " + toDate[0]}

#Upgrade References & Companies txt File
#In case It would be Erased, It would be created
try: 
	#Backup
	copyfile(RPATH, RBPATH)
	#New entry
	with open(RPATH, 'a') as refer:
		refer.write("\n")
		json.dump(ref, refer)
	logD.info('References Dictionary Correctly Updated')
except: 
	#Create new references file
	with open(RPATH, 'w') as refer:
		json.dump(ref, refer)
	logD.info('References Dictionary was not Found')
	logD.info('A new References Dictionary was Created')
	logD.info('Check possibles Errors.Restablish Backup if It would be necessary')
	
try: 
	#Backup
	copyfile(CPATH, CBPATH)
	#Add Company if it is not found
	with open(CPATH, 'r') as c:
		comp = json.load(c)
	for i in range(0, len(companies)):
		if companies[i] not in comp:
			comp.append(companies[i])
	outfile = open(CPATH, 'w')
	json.dump(comp, outfile)
	logD.info('Companies Dictionary Correctly Updated')
except: 
	#Create new companies file
	outfile = open(CPATH, 'w')
	json.dump(companies, outfile)
	logD.info('Companies Dictionary was not Found')
	logD.info('A new Companies Dictionary was Created')
	logD.info('Check possibles Errors.Restablish Backup if It would be necessary')

logD.info('Process Finished...')