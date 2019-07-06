import os

from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dmsuMarket.settings.dev'

celery_app = Celery("sms")
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks(['celery_tasks.sms'])

if __name__ == '__main__':
    celery_app.start()
