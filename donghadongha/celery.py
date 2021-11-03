import os

from celery import Celery
from donghadongha import settings

# Celery 모듈을 위한 Django 기본세팅
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donghadongha.settings')

# app = Celery('donghadongha',
#              broker='amqp://',
#              backend='rpc://',
#              include=['coin.tasks'])

app = Celery('test')

from donghadongha import celeryconfig
from celery.schedules import crontab


app.config_from_object(celeryconfig)

app.conf.beat_schedule = {
    'every-15-second': {
        'task': 'coin.tasks.updateMarkCap',
        'schedule': crontab(minute='17', hour='16, 20'),
        'args': ()
    },
}

app.conf.update(
    result_expires=3600,
)

app.autodiscover_tasks(settings.INSTALLED_APPS)


if '__main__' == __name__:
    app.start()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

