from celery import Celery
app=Celery('Virtual_IoT_Lab',broker='redis://localhost/0')
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "Virtual_IoT_Lab.settings"
@app.task
def hello():
  return 'Hello I am in windows'
