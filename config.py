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
	WHERE repo_name = '?';""" % TABLE_QUEUE
	
TABLE_QUEUE_INSERT = """
UPDATE """	
	
TABLE_QUEUE_UPDATE = """
UPDATE """

TABLE_REPOSITORY_CREATE = """
CREATE TABLE %s (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT,
	description TEXT,
	last_commit TEXT,
	date TEXT);""" % TABLE_REPOSITORY