import pyodbc
import json
import datetime

with open('C:\\Users\\daWigs\\Desktop\\Database\\Json\\gYYLbjXvHnP4dV4C - (From Mon Oct 29 06.41.55 +0000 2018 To Wed Apr 03 22.28.57 +0000 2013)(1).json', 'r') as f: 
	data = json.load(f)
	
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\daWigs\Documents\Project Database.accdb;')
cursor = conn.cursor()


id = []

for i in range(0,len(data)):

	if  data[i]['user']['id'] == 740233567842795520:
	
		try:
				name = data[i]['user']['name']
				name = name.replace("'"," ")
				location = data[i]['user']['location']
				url = data[i]['user']['url']
				
				date = datetime.datetime.strptime(data[i]['user']['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
					
				if 	location == None: 
					location = '-'
					
				if 	url == None: 
					url = '-'
					
					
				cursor.execute("INSERT INTO Companies (IDCompany, nameCompany, screenName, accountCreated_at, Location, url) VALUES(" + str(data[i]['user']['id']) + ",'" + name + "','" + str(data[i]['user']['screen_name']) + "','" + str(date) + "','" + location + "','" + url + "')")
				
				id = [id, data[i]['user']['id']]
			
		except: 
			print('error')
			
	
conn.commit()
conn.close()