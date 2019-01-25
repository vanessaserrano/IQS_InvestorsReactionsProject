import pyodbc
import json
import datetime

with open('C:\\Users\\daWigs\\Desktop\\Database\\Json\\gYYLbjXvHnP4dV4C - (From Mon Oct 29 06.41.55 +0000 2018 To Wed Apr 03 22.28.57 +0000 2013)(2).json', 'r') as f: 
	data = json.load(f)
	
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\daWigs\Documents\Project Database.accdb;')
cursor = conn.cursor()

id = []

for i in range(0,len(data)):

	if not data[i]['id'] in id:
	
		try:
			tweet = ""
			rt = 0
			rp = 0

			try:
				tweet = data[i]['retweeted_status']['extended_tweet']['full_text']
				rt = -1
			except:
				try:
					tweet = data[i]['retweeted_status']['text']
					rt = -1
				except:
					try:
						tweet = data[i]['extended_tweet']['full_text']
					except:
						tweet = data[i]['text']
						
			if 'RT' in tweet: 
				rt = -1

			if data[i]['in_reply_to_user_id'] != None:
				rp = -1
				
			date = datetime.datetime.strptime(data[i]['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
			
			tweet = tweet.replace("’"," ")
			tweet = tweet.replace("'"," ")
			
			print("INSERT INTO Tweets (IDTweet, Tweet, created_at, url, IDCompany, Replay, Retweet, Retweets, Replies, Favorite) VALUES(" + str(data[i]['id']) + ",'" + tweet + "','" + str(date) + "','" + "https://twitter.com/statuses/" + data[i]['id_str'] + "'," + str(data[i]['user']['id']) + "," + str(rp) + "," + str(rt) + "," + str(data[i]['retweet_count']) + "," + str(data[i]['reply_count']) + "," + str(data[i]['favorite_count']) + ")")
				
				
			cursor.execute("INSERT INTO Tweets (IDTweet, Tweet, created_at, url, IDCompany, Replay, Retweet, Retweets, Replies, Favorite) VALUES(" + str(data[i]['id']) + ",'" + tweet + "','" + str(date) + "','" + "https://twitter.com/statuses/" + data[i]['id_str'] + "'," + str(data[i]['user']['id']) + "," + str(rp) + "," + str(rt) + "," + str(data[i]['retweet_count']) + "," + str(data[i]['reply_count']) + "," + str(data[i]['favorite_count']) + ")")
			
			id = [id, data[i]['id']]
			
		except:
			print("error")
	
conn.commit()
conn.close()
