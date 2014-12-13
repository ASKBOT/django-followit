import os, sys
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'followit.tests.settings'
import django
try:
    django.setup()
except AttributeError:  # django < 1.7
    pass
from django.test.runner import DiscoverRunner
failures = DiscoverRunner().run_tests(['tests.FollowerTests',], verbosity = 1)
if failures:
    sys.exit(failures)
