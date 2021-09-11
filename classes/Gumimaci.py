from github import Github
import config
import sqlite3


class Gumimaci(object):
	def __init__(
		self,
		_personal_access_token):
		
		self._personal_access_token = _personal_access_token
		self._github = None
        
		self._database = config.DATABASE
		self._database_table_queue = config.TABLE_QUEUE
		self._database_table_repository = config.TABLE_REPOSITORY
		self._db_conn = None

	def connect(
		self):
		
		self._github = Github(
			self._personal_access_token)
            
		self._db_conn = sqlite3.connect(
			self._database)
	
	
	def select(
		self,
		_table,
		_repo_name = None):
		
		cursor = self._db_conn.cursor()
		
		if _repo_name == None:
			cursor.execute(
				_table)
		else:
			cursor.execute(
				_table,
				(_repo_name,))
			
		return cursor.fetchall()