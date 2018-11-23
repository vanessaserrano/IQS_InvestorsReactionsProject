import requests
import ast
from requests_oauthlib import OAuth1
import json
import os
import sys

class getQuery:

	def __init__(self, logD):

		#Log
		self.logD = logD
	
	def OAuth(self):
		
		#PATH Credentials
		PATHC = os.path.join(os.path.dirname(sys.path[0]), 'Credentials.txt')
		
		#Read Credentials
		try:
			with open(PATHC, 'r') as Cr:
				s = Cr.read()
				credentials = ast.literal_eval(s)
				Cr.close()
				self.logD.info('Credentials Successfully Uploaded')
		except SyntaxError: 
			self.logD.error('Credentials Incorrectly Introduced')
			self.logD.error('Check Introduced Credentials. Restart the Program')
			raise
		except FileNotFoundError: 
			self.logD.error('Credentials File not Found')
			self.logD.error('Restart the Program')
			raise

		#Parameters
		self.consumer_key = credentials["consumer_key"]
		self.consumer_secret = credentials["consumer_secret"]
		access_token = credentials["access_token"]
		access_token_secret = credentials["access_token_secret"]
		self.devEnv = credentials["DevEnvironment"]
		
		#Authentication
		auth = OAuth1(self.consumer_key, self.consumer_secret, access_token, access_token_secret)
		self.session = requests.Session()
		self.session.auth = auth
		
	def getParam(self):
		
		#PATH Request Parameters
		PATHR = os.path.join(os.path.dirname(sys.path[0]), 'Request Parameters.txt')
		
		#URL
		LOOKUP_URL = 'https://api.twitter.com/1.1/users/lookup.json'
		
		#Read Parameters
		try:	
			with open(PATHR, 'r') as f:
				t = f.read()
				parameters = ast.literal_eval(t)
				f.close()
				self.logD.info('Parameters Successfully Uploaded')
		except SyntaxError: 
			self.logD.error('Parameters Incorrectly Introduced')
			self.logD.error('Check Introduced Parameters. Restart the Program')
			raise
		except FileNotFoundError: 
			self.logD.error('Parameters File not Found')
			self.logD.error('Restart the Program')
			raise

		output = []

		#Screen Names to IDs
		for i in range(0, len(parameters['companies'])):
			params = {'screen_name': parameters['companies'][i]}
			try:
				response = self.session.request('GET', LOOKUP_URL, params=params).json()
				self.logD.info('Successfully Converted: ' + response[0]['screen_name'])
				output.append([parameters['companies'][i],response[0]['id_str']])
			except requests.exceptions.ConnectionError:
				self.logD.error('Connection Error - IDs')
				raise
			except KeyError:
					#Failed Download
					self.logD.error('Failed Download Request')
					self.logD.debug('--------------------------------------------------------------------------------------------------')
					self.logD.error(response)
					self.logD.debug('--------------------------------------------------------------------------------------------------')
					self.logD.info('Incorrectly Converted: ' + parameters['companies'][i])
					self.logD.info('Restart the Program')
					raise
					
		output = [output, parameters['toDate'], parameters['fromDate'], self.consumer_key, self.consumer_secret, self.devEnv]
		
		
		return output
