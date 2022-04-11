import os

from django.conf import settings

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poke.settings.local')

app = Celery('poke')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS,)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

