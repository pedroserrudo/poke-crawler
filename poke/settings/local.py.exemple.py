from poke.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}