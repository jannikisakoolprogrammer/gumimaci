from classes.GumimaciScheduler import GumimaciScheduler

personal_access_token = {
	"personal_access_token": "NO_THIS_WONT_WORK_SORRY!"}

scheduler = GumimaciScheduler(personal_access_token)
scheduler.connect()
scheduler.run()

