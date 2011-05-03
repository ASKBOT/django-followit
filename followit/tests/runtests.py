import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'followit.tests.settings'
from django.test.simple import run_tests
failures = run_tests(['tests.FollowerTests',], verbosity = 1)
if failures:
    sys.exit(failures)
