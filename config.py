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
	
TABLE_QUEUE_SELECT = """
SELECT * FROM %s
	WHERE repo_name = ?
	ORDER BY rowid ASC;""" % TABLE_QUEUE
	
TABLE_QUEUE_SELECT_ALL = """
SELECT * FROM %s
	ORDER BY rowid ASC;""" % TABLE_QUEUE	
	
TABLE_QUEUE_INSERT = """
INSERT INTO %s 
VALUES(
	?,
	?);""" % TABLE_QUEUE
	
TABLE_QUEUE_DELETE = """
DELETE FROM %s
	WHERE repo_name = ?;""" % TABLE_QUEUE

TABLE_REPOSITORY_CREATE = """
CREATE TABLE %s (
	repo_name TEXT PRIMARY KEY,
	description TEXT,
	last_commit TEXT,
	date TEXT);""" % TABLE_REPOSITORY

TABLE_REPOSITORY_SELECT = """
SELECT * FROM %s
	WHERE repo_name = ?""" % TABLE_REPOSITORY
	
TABLE_REPOSITORY_INSERT = """
INSERT INTO %s VALUES (?, ?, ?, ?);""" % TABLE_REPOSITORY

TABLE_REPOSITORY_DELETE = """
DELETE FROM %s
	WHERE repo_name = ?;""" % TABLE_REPOSITORY
	
TABLE_REPOSITORY_UPDATE = """
UPDATE TABLE %s
SET description = ?,
	last_commit = ?,
	date = ?;""" % TABLE_REPOSITORY
	
	
DIRECTORY_REPOSITORIES = "repositories"