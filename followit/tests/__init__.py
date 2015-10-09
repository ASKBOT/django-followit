from django.apps import AppConfig, apps
from django.contrib.auth import get_user_model

class TestConfig(AppConfig):
    name = 'followit.tests'

    def ready(self):
        import followit
        Car = apps.get_model('tests.Car')
        Alligator = apps.get_model('tests.Alligator')
        followit.register(Car)
        followit.register(Alligator)
        followit.register(get_user_model())#to test following users

default_app_config = 'followit.tests.TestConfig'
