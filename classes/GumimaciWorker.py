from classes.Gumimaci import Gumimaci
from classes.Repository import Repository
import config
import sys
from github.GithubException import *
import subprocess
import os.path
import shutil
import datetime
import time
import importlib.util


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
		
		# A "gumimaci" file must exist.
		gumimaci_repo_file = "gumimaci"

		for row in rows_queue:
			repo = self._github.get_user().get_repo(
				row[0])
				
			try:
				content_file = repo.get_contents(
					gumimaci_repo_file)
					
			except: # Exception:
				#UnknownObjectException("status", "data", "headers")
				#print("file '%s' not found in repo '%s'" % (
				#	gumimaci_repo_file,
				#	repo.name))
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
				 
			# Do validation.
			if sys.platform == "win32":
				subprocess.run(
					["nose2",
					 "-v"])
			else:
				subprocess.run(
					["nose2-3",
					 "-v"])	
				 
			path1 = os.path.join(
				os.getcwd(),
				"version.py")
				 
			spec = importlib.util.spec_from_file_location("version.py", path1)			
			version = importlib.util.module_from_spec(spec)
			spec.loader.exec_module(version)
				
			# Create an executable.
			if sys.platform == "win32":
				subprocess.run(
					["python",
					 "setup.py",
					 "bdist_msi"])
			elif sys.platform == "linux":
				subprocess.run(
					["python3",
					 "setup.py",
					 "build"])
			
			# Only create a release for now.
			dt = datetime.datetime.now().strftime(
						"%Y_%m_%d_%H_%M_%S")
						
			git_release = repo.create_git_release(
				"%s_%s_%s" % (
					repo.name,
					version.VERSION,
					sys.platform),
				"%s_%s_%s" % (
					repo.name,
					version.VERSION,
					sys.platform),
				row[2],
				False,
				False,
				row[1])
			
			# For windows and linux:  Zip "build" directory.
			b_path = os.path.join(
				os.getcwd(),
				"build")
			p = shutil.make_archive(
				sys.platform,
				"zip",
				root_dir = b_path)
			
			# Upload zip (no installer needed)
			git_release.upload_asset(
				p,
				label="%s_%s_%s" % (
					repo.name,
					version.VERSION,
					sys.platform))
			
			# Upload installer.
			d_path = os.path.join(
				os.getcwd(),
				"dist")
			if os.path.exists(d_path):
				files = os.listdir(d_path)
				if len(files) > 0:
					for f in files:
						installer_path = os.path.join(
							d_path,
							f)
						
						git_release.upload_asset(
							installer_path,
							label = f)				
			
			# Go back two levels.
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
			
			# Always sleep 5 minutes between creating a new release.
			time.sleep(60)