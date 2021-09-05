from github import Github


class Gumimaci(object):
	def __init__(
		self,
		_personal_access_token):
		
		self._personal_access_token = _personal_access_token
		self._github = None		


	def connect(
		self):
		
		self._github = Github(
			self._personal_access_token)