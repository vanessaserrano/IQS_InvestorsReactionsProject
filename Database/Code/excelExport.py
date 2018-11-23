import json
import xlsxwriter
import datetime
import os
import sys


class JsonToExcel:

	def __init__(self, data, ID):
	
		#Data Parameters
		self.data = data[0]
		self.ID = ID
		
		#PATH Definition
		CPATH = os.path.join(os.path.dirname(sys.path[0]),'References', 'Companies Dictionary.txt')
		
		with open(CPATH, 'r') as f: 
			companies = json.load(f)
		
		#ID --> Company Name
		for i in range(0, len(companies)):
			if companies[i][1] == ID:
				title = os.path.join(os.path.dirname(sys.path[0]),'Excel', companies[i][0] + " - " + datetime.datetime.now().strftime("%Y-%m-%d") + " .xlsx")
				
			
		#Create .xlsx
		self.workbook = xlsxwriter.Workbook(title)
		self.worksheetInfo = self.workbook.add_worksheet('Info')
		self.worksheetData = self.workbook.add_worksheet('Data')
		
		#Titles
		self.worksheetData.write(0, 0, 'Fecha')
		self.worksheetData.write(0, 1, 'Id Tweet')
		self.worksheetData.write(0, 2, 'Tweet')
		self.worksheetData.write(0, 3, 'URL Tweet')
		self.worksheetData.write(0, 4, 'Idioma Tweet')
		self.worksheetData.write(0, 5, 'Retweeted')
		self.worksheetData.write(0, 6, 'Retweets')
		self.worksheetData.write(0, 7, 'Quote')
		self.worksheetData.write(0, 8, 'Replay')
		self.worksheetData.write(0, 9, 'Favourite')
		
		self.worksheetInfo.write(0, 0, 'Información')
		self.worksheetInfo.write(1, 0, 'Empresa')
		self.worksheetInfo.write(2, 0, 'Id Twitter')
		self.worksheetInfo.write(3, 0, 'Fecha Creación')
		self.worksheetInfo.write(4, 0, 'Location')
		self.worksheetInfo.write(5, 0, 'Followers')
		self.worksheetInfo.write(6, 0, 'Friends')
		self.worksheetInfo.write(7, 0, 'Tweets')
		
		
		print('Excel Created...')

	def export(self):
	
		print('\nExporting Started...\n')
		
		n = 1
		
		for i in range(0, len(self.data)): 
			if self.data[i]['user']['id_str'] == self.ID:
				for j in range(0, 10):
					try:
						if j == 0:
								self.worksheetData.write(n, j, self.data[i]['created_at'])
						elif j == 1:
								self.worksheetData.write(n, j, self.data[i]['id_str'])
						elif j == 2:
							try:
								self.worksheetData.write(n, j, self.data[i]['retweeted_status']['extended_tweet']['full_text'])	
								self.worksheetData.write(n, 5, 'Yes')
							except:
								try:
									self.worksheetData.write(n, j, self.data[i]['retweeted_status']['text'])
									self.worksheetData.write(n, 5, 'Yes')
								except:
									try:
										self.worksheetData.write(n, j, self.data[i]['extended_tweet']['full_text'])
										self.worksheetData.write(n, 5, 'No')
									except:
										self.worksheetData.write(n, j, self.data[i]['text'])
										self.worksheetData.write(n, 5, 'No')
									
						elif j == 3:
							self.worksheetData.write(n, j,  "https://twitter.com/statuses/" + self.data[i]['id_str'])
						elif j == 4:
							self.worksheetData.write(n, j, self.data[i]['lang'])
						elif j == 6:
							self.worksheetData.write(n, j, self.data[i]['retweet_count'])
						elif j == 7:
							self.worksheetData.write(n, j, self.data[i]['quote_count'])
						elif j == 8:
							self.worksheetData.write(n, j, self.data[i]['reply_count'])
						elif j == 9:
							self.worksheetData.write(n, j, self.data[i]['favorite_count'])
							
					except: 
						print("Tweet ID: " + self.data[0]['id_str'] + " could not be exported")
				n = n + 1	
				index = i		
		
		#Company Info
		self.worksheetInfo.write(1, 1, self.data[index ]['user']['name'])
		self.worksheetInfo.write(2, 1, self.data[index ]['user']['id'])
		self.worksheetInfo.write(3, 1, self.data[index ]['user']['created_at'])
		self.worksheetInfo.write(4, 1, self.data[index ]['user']['location'])
		self.worksheetInfo.write(5, 1, self.data[index ]['user']['followers_count'])
		self.worksheetInfo.write(6, 1, self.data[index ]['user']['friends_count'])
		self.worksheetInfo.write(7, 1, self.data[index ]['user']['statuses_count'])


				
		self.workbook.close()
		
		print('Exporting Finished...')

		