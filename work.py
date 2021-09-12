from classes.GumimaciWorker import GumimaciWorker
import secret
import time


personal_access_token = {
	"personal_access_token": secret.GITHUB_TOKEN}

scheduler = GumimaciWorker(personal_access_token)
scheduler.connect()
#while True:
scheduler.run()
# Always sleep 5 minutes before starting a new run.
#time.sleep(300)

