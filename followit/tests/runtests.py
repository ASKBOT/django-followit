import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'followit.tests.settings'
from django.test.simple import run_tests
failures = run_tests(['followit.tests.FollowerTests',], verbosity=9)
if failures:
    sys.exit(failures)
