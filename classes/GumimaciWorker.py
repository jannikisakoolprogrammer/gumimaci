from classes.Gumimaci import Gumimaci
from classes.Repository import Repository
import config
import sys
from github.GithubException import *
import subprocess
import os.path
import shutil
import datetime


class GumimaciWorker(Gumimaci):
	def __init__(
		self,
		_args):
				
		super(
			GumimaciWorker,
			self).__init__(
				_args["personal_access_token"])
	
	
	def update_repository(
		self,
		_repo_name,
		_sha,
		_date):
		
		cursor = self._db_conn.cursor()
		cursor.execute(
			config.TABLE_REPOSITORY_UPDATE,
			(_sha,
			 _date,
			 _repo_name))
		
		self._db_conn.commit()
	
	
	def delete_queue(
		self,
		_sha):
		
		cursor = self._db_conn.cursor()
		cursor.execute(
			config.TABLE_QUEUE_DELETE,
			(_sha,))
		
		self._db_conn.commit()
	
	
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
			
			local_repositories_path = os.path.join(
					os.getcwd(),
					config.DIRECTORY_REPOSITORIES)
				
			os.chdir(local_repositories_path)
				
			subprocess.run(
				["git",
				 "clone",
				 url])
				 
			os.chdir(repo.name)
			
			subprocess.run(
				["git",
				 "status"])
			
			# Checkout specific commit.
			subprocess.run(
				["git",
				 "checkout",
				 row[1]])
				 
			# Do validation, build, package and create a release.
			# Only create a release for now.
			dt = datetime.datetime.now().strftime(
						"%Y_%m_%d_%H_%M_%S")
						
			repo.create_git_release(
				"%s%s" % (
					repo.name,
					dt),
				"%s%s" % (
					repo.name,
					dt),
				row[2],
				False,
				False,
				row[1])
			
			# Go back on level.
			os.chdir("..")
			os.chdir("..")
				 
			# Remove repository.
			path_to_repo = os.path.join(
				os.getcwd(),
				config.DIRECTORY_REPOSITORIES,
				row[0])
				
			shutil.rmtree(
				path_to_repo)
			
			# TODO:  Update "repository" table
			self.update_repository(
				repo.name,
				row[1],
				dt)
				
			# TODO:  Remove entry from "queue" table.
			self.delete_queue(
				row[1])