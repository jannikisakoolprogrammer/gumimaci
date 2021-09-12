class Repository(object):
	def __init__(
		self,
		_name,
		_description,
		_new_commits):
		
		self._name = _name
		self._description = _description
		self._new_commits = _new_commits
	
	
	def get_name(
		self):
		
		return self._name
	
	
	def get_description(
		self):
		
		return self._description
	
	
	def get_new_commits(
		self):
		
		return self._new_commits
	
	
	def get_last_commit(
		self):
		
		return self._new_commits[0]
	
	
	def get_recent_commits(
		self,
		_root):
		
		l = []
		x = 0
		y = 0
		
		
		
		for commit in self._new_commits:
			if commit.sha == _root[0][2]:
				break
			else:
				x += 1
		
		for y in range(0, x, 1):
			l.append(
			[self._new_commits[y].sha,
			 self._new_commits[y].commit.message])
			
		return l