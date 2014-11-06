import os

DIRNAME = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : ':memory:',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'followit',
    'followit.tests'
)

SECRET_KEY = '1234567890'
