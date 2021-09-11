from classes.Gumimaci import Gumimaci
from classes.Repository import Repository
import config
import sys
from github.GithubException import *
import subprocess


class GumimaciWorker(Gumimaci):
	def __init__(
		self,
		_args):
				
		super(
			GumimaciWorker,
			self).__init__(
				_args["personal_access_token"])
	
	
	def run(
		self):
		
		rate = self._github.get_rate_limit()
		print(rate)		
		
		# Build everyting in queue.
		# Delete record from queue after being processed.
		rows_queue = self.select(
			config.TABLE_QUEUE_SELECT_ALL)
			
		if sys.platform == "win32":
			gumimaci_repo_file = "gumimaci_windows.yaml"
		elif sys.platform == "linux":
			gumimaci_repo_file = "gumimaci_linux.yaml"
		
		for row in rows_queue:
			repo = self._github.get_user().get_repo(
				row[0])
			
			print(repo)
				
			try:
				content_file = repo.get_contents(
					gumimaci_repo_file)
					
			except: # Exception:
				#UnknownObjectException("status", "data", "headers")
				print("file '%s' not found in repo '%s'" % (
					gumimaci_repo_file,
					repo.name))
				continue
			
			# Now check out the repository.
			# We use git for it.
			url = "https://github.com/%s.git" % (
				repo.full_name,)
				
			subprocess.run(
				["cd",
				 config.DIRECTORY_REPOSITORIES])
				
			subprocess.run(
				["git",
				 "clone",
				 url])
			
			# Go back on level.
			subprocess.run(
				["cd",
				 ".."]
				 
			# Remove repository.
			subprocess.run(
				["rmdir",
				 row[0]])