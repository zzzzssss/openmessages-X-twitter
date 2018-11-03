import psycopg2
from config.config import Config

class DBConnect:
	def __init__(self):
		""" Connect to the PostgreSQL database server """
		conn = None
		try:
			# read connection to postgresql section parameters
			params = Config('config.ini', 'postgresql').getConfig()
			# connect to the PostgreSQL server
			print('Connecting to the PostgreSQL database...')
			conn = psycopg2.connect(**params)
			print('Connected to the PostgreSQL database...')
			self.conn = conn
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def getDB(self):
		return self.conn

	def closeDB(self):
		self.conn.close()
