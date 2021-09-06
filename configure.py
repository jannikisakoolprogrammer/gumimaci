# This script configures gumimaci, so it can be used.
import sqlite3
import logging

import config

logging.basicConfig(
	level = logging.INFO)

connection = sqlite3.connect(config.DATABASE)
cursor = connection.cursor()

# Create the tables now.
logging.info("Creating tables...")
cursor.execute(config.TABLE_QUEUE_CREATE)
cursor.execute(config.TABLE_REPOSITORY_CREATE)

connection.commit()

connection.close()
logging.info("Creating tables finished")
logging.info("Script executed successfully.  You may now start using gumimaci.")