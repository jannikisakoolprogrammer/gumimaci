# This script configures gumimaci, so it can be used.
import sqlite3
import logging

logging.basicConfig(
	level = logging.INFO)

# There are two tables in the database "db.sqlite":
# - queue
# - repository

DATABASE = "db.sqlite"
TABLE_QUEUE = "queue"
TABLE_REPOSITORY = "repository"

TABLE_QUEUE_CREATE = """
CREATE TABLE %s (
	repo_name TEXT,
	last_commit TEXT);""" % TABLE_QUEUE

TABLE_REPOSITORY_CREATE = """
CREATE TABLE %s (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	description TEXT,
	last_commit TEXT,
	date TEXT);""" % TABLE_REPOSITORY

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Create the tables now.
logging.info("Creating tables...")
cursor.execute(TABLE_QUEUE_CREATE)
cursor.execute(TABLE_REPOSITORY_CREATE)

connection.commit()

connection.close()
logging.info("Creating tables finished")
logging.info("Script executed successfully.  You may now start using gumimaci.")