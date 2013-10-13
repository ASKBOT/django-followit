import os
import sys

RUNTESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, os.path.dirname(RUNTESTS_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = 'followit.tests.settings'

from followit.tests import settings
from django.test.utils import get_runner

TestRunner = get_runner(settings)
test_runner = TestRunner(interactive=False)
failures = test_runner.run_tests(['tests.FollowerTests'])

if failures:
    sys.exit(failures)

