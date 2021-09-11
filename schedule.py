from classes.GumimaciScheduler import GumimaciScheduler
import secret


personal_access_token = {
	"personal_access_token": secret.GITHUB_TOKEN}

scheduler = GumimaciScheduler(personal_access_token)
scheduler.connect()
scheduler.run()

