import random
import time

from ..main import celery_app

@celery_app.task(name='send_sms_code')
def send_sms_code(*args):
    time.sleep(random.randint(0,2))
    print('>>>>>>>>>>>>Clouds Communicating>>>>>>>>>>>>>>')
    print('%s>>>>>>>>>>>>>>>>>>>>>>%s' % args)
