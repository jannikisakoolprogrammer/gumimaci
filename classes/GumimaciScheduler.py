from classes.Gumimaci import Gumimaci
import sys
from github.GithubException import *

class GumimaciScheduler(Gumimaci):
	def __init__(
		self,
		_args):
				
		super(
			GumimaciScheduler,
			self).__init__(
				_args["personal_access_token"])
	
	
	def run(
		self):
		
		rate = self._github.get_rate_limit()
		print(rate)
		
		# Go through all repos, and only take into account those, that have a 
		# "gumimaci_linux.yaml" or "gumimaci_windows.yaml" file in the root dir.
		
		if sys.platform == "win32":
			gumimaci_repo_file = "gumimaci_windows.yaml"
		elif sys.platform == "linux":
			gumimaci_repo_file = "gumimaci_linux.yaml"
		
		if gumimaci_repo_file != "":
			for repo in self._github.get_user().get_repos():
				try:
					content_file = repo.get_contents(
						gumimaci_repo_file)
						
				except: # Exception:
					#UnknownObjectException("status", "data", "headers")
					print("file '%s' not found in repo '%s'" % (
						gumimaci_repo_file,
						repo.name))
					continue
						
				# Now fetch the last commit id.
				commits = repo.get_commits()
				if commits.totalCount > 0:
					last_commit_sha = commits[0].sha
					print(last_commit_sha)

					# TODO:  Now create or udpate an existing repository record in the "queue" table.
					# TODO:  But first look if we need to actually build a new version of the repo (check the table 'repository' first for "name" and "sha".