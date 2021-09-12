from classes.GumimaciScheduler import GumimaciScheduler
import secret
import time


personal_access_token = {
	"personal_access_token": secret.GITHUB_TOKEN}

scheduler = GumimaciScheduler(personal_access_token)
scheduler.connect()
while True:
	scheduler.run()
	time.sleep(60)

