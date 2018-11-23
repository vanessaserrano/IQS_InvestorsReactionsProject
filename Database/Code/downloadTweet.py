import requests
import json




class tweets:

	def __init__(self, consumer_key, consumer_secret, logD, env):
		#Authentication keys for Tweeter Api
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		
		#Add Log 
		self.logD = logD
		
		self.logD.info('Connection Started...')
		
		#Last date downloaded
		self.lastDown = ""
		
		#Env full-archive or 30 days
		self.env = env
		
		
	#Authentication function
	def auth(self):	
	
		#Parameters
		OAUTH_ENDPOINT = 'https://api.twitter.com/oauth2/token'
		data = [('grant_type', 'client_credentials')]
		
		#API Request
		try:
			resp = requests.post(OAUTH_ENDPOINT, data=data, auth=(self.consumer_key, self.consumer_secret))
		except requests.exceptions.ConnectionError:
			self.logD.error('Connection Error - Authentication')
			self.logD.info('Restart the Program')
			raise
		except socket.timeout:
			self.logD.error('Timeout - Authentication')
			self.logD.info('Restart the Program')
			raise
		
		token = resp.json()
		
		#Bearer Token 
		try:
			self.bearer = "Bearer " + token['access_token']
			self.logD.info('Authentication Correct')
			
		except KeyError: 
			#Authentication fail due to an error with the keys
			self.logD.error('Failed Authentication Request')
			self.logD.debug('--------------------------------------------------------------------------------------------------')
			self.logD.error(token)
			self.logD.debug('--------------------------------------------------------------------------------------------------')
			self.logD.info('Check Keys. Restart the Program')
			raise
			
			
	#Download tweet function	 
	def download(self, query):	
	
		#Parameters
		#endpoint full-archive
		endpoint = "https://api.twitter.com/1.1/tweets/search/fullarchive/" + self.env + ".json"
		#endpont 30 days
		#endpoint = "https://api.twitter.com/1.1/tweets/search/30day/" + self.env + ".json" 
		headers = {"Authorization": self.bearer, "Content-Type": "application/json"}  
		
		#Request
		try:
			results = requests.post(endpoint,data=query,headers=headers).json()
		except requests.exceptions.ConnectionError:
			self.logD.error('Connection Error - Download')
			self.logD.info('Last downloaded date: ' + self.lastDown + ' & query: ' + query)
			self.logD.info('Restart the Program')
			raise
		except socket.timeout:
	
			self.logD.error('Timeout - Download')
			self.logD.info('Last downloaded date: ' + self.lastDown + ' & query: ' + query)
			self.logD.info('Restart the Program')
			raise
		
			
		#Returne Data
		try: 
			#Next Data (Next Code)
			if len(results) == 3:
				self.lastDown =  results['results'][0]['created_at']
				self.logD.info('Successfully downloaded --> From: ' + results['results'][-1]['created_at'] + ' To: ' + results['results'][0]['created_at'])
			return [0 , results['results'], results['next'], results["requestParameters"]["maxResults"]]
		except KeyError:
			try:
				try:
					#First or Last Data (No Next Code)
					self.lastDown =  results['results'][0]['created_at']
					self.logD.info('Successfully downloaded --> From: ' + results['results'][-1]['created_at'] + ' To: ' + results['results'][0]['created_at'])
					return [0 , results['results'], results["requestParameters"]["maxResults"]]
				except IndexError:
					#No Data
					self.logD.error('Failed Download Request')
					self.logD.info('No Data Avaiable for these Dates')
					self.logD.info('Restart the Program')
					raise
					
			except KeyError:
				#Failed Download
				self.logD.error('Failed Download Request')
				self.logD.debug('--------------------------------------------------------------------------------------------------')
				self.logD.error(results)
				self.logD.debug('--------------------------------------------------------------------------------------------------')
				self.logD.info('Last downloaded date: ' + self.lastDown + ' & query: ' + query)
				self.logD.info('Restart the Program')
				raise
	