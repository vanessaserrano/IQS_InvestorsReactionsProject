import logging 
import os
import sys
import datetime

class logs: 

	def __init__(self, code):
	
		#Saving PATH
		PATH = os.path.join(os.path.dirname(sys.path[0]),'Logs', code + ' - ' + datetime.datetime.now().strftime("%Y%m%d - %Hh%Mm%Ss") + '.log')
	
		#Create the Logger 
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.DEBUG)
		
		#Create the Handler for logging data to file
		self.logger_handler = logging.FileHandler(PATH)
		self.logger_stream = logging.StreamHandler(sys.stdout)
		self.logger_handler.setLevel(logging.DEBUG)
		self.logger_stream.setLevel(logging.DEBUG)
		
		#Creat a Formatter for formatting the log messages
		self.logger_formatter = logging.Formatter('%(levelname)s - %(message)s - %(asctime)s', "%Y-%m-%d %H:%M:%S")
		
		#Add the Formatter to the Handler
		self.logger_handler.setFormatter(self.logger_formatter)
		self.logger_stream.setFormatter(self.logger_formatter)
		
		#Add the Handler to the Logger 
		self.logger.addHandler(self.logger_stream)
		self.logger.addHandler(self.logger_handler)
		file = os.path.basename(os.path.normpath(PATH))
		self.logger.info('Log ' + file + ' created')

		
	def info(self, mssg): 
		self.logger.info(mssg)
		
	def error(self, mssg): 
		self.logger.error(mssg)
	
	def debug(self, mssg): 
		self.logger.debug(mssg)
		