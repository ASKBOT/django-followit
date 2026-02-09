import random
import string

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    },
}

MIDDLEWARE_CLASSES = ()

SECRET_KEY = ''.join([random.choice(string.ascii_letters) for x in range(40)])

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'followit',
    'followit.tests'
)
