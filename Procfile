web: gunicorn --bind :8000 poke.settings.wsgi:application
worker: celery worker -A poke.settings.celery.app -l debug --scheduler django_celery_beat.schedulers.DatabaseScheduler
beat: celery beat -A poke.settings.celery.app -l debug --scheduler django_celery_beat.schedulers.DatabaseScheduler
