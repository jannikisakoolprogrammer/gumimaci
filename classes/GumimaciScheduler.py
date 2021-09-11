from classes.Gumimaci import Gumimaci
from classes.Repository import Repository
import config
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
				
	def insert_queue(
		self,
		_repo_name,
		_commit,
		_message):
		
		cursor = self._db_conn.cursor()
		cursor.execute(
			config.TABLE_QUEUE_INSERT,
			(_repo_name,
			 _commit,
			 _message))
		
		self._db_conn.commit()
	
	
	def insert_repository(
		self,
		_repo_name,
		_description,
		_commit,
		_date):
		
		cursor = self._db_conn.cursor()
		cursor.execute(
			config.TABLE_REPOSITORY_INSERT,
			(_repo_name,
			 _description,
			 _commit,
			 _date))
			 
		self._db_conn.commit()
	
	
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
					
				# Store important information.
				repository = Repository(
					repo.name,
					repo.description,
					repo.get_commits())
					
				if repository.get_new_commits().totalCount > 0:
					
					row_repository = self.select(
						config.TABLE_REPOSITORY_SELECT,
						repository.get_name())
						
					# If the repo does not yet exist, only use the last sha as the root.
					if len(row_repository) == 0:
						# Create new repository entry.
						self.insert_repository(
							repository.get_name(),
							repository.get_description(),
							repository.get_last_commit().sha,
							repository.get_last_commit().commit.committer.date)
							
						# Make sure the build is not yet queued.  It shouldn't be.
						rows_queue = self.select(
							config.TABLE_QUEUE_SELECT,
							repository.get_name())

						if len(rows_queue) == 0:
							# Add a new commit to be build.
							self.insert_queue(
								repository.get_name(),
								repository.get_last_commit().sha,
								repository.get_last_commit().commit.message)
						
					else:
						# Otherwise we add all new commits since the last build, given that they are not in the queue yet.
						row_repository = self.select(
							config.TABLE_REPOSITORY_SELECT,
							repository.get_name())
							
						if len(row_repository) > 0:
							recent_commits = repository.get_recent_commits(
								row_repository)
							
							# Oldest to newest.
							reversed(recent_commits)
							
							# Fetch all repository build queue records.
							rows_queue = self.select(
								config.TABLE_QUEUE_SELECT,
								repository.get_name())
							
							list_rows_queue = []
							for x in rows_queue:
								list_rows_queue.append(x[1])
							
							for commit in recent_commits:
								# Make sure the current commit does not yet exist in the queue.  Otherwise, don't add it.
								if commit[0] in list_rows_queue:
									continue
								else:
									# Add a new commit to be build.
									self.insert_queue(
										repository.get_name(),
										commit[0],
										commit[1])