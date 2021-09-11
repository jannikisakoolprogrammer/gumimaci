from classes.GumimaciWorker import GumimaciWorker
import secret


personal_access_token = {
	"personal_access_token": secret.GITHUB_TOKEN}

scheduler = GumimaciWorker(personal_access_token)
scheduler.connect()
scheduler.run()

