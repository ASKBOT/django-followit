from django.db import models
from followit.compat import get_user_model

class Car(models.Model):
    yeah = models.BooleanField(default = True)

class Alligator(models.Model):
    yeah = models.BooleanField(default = True)

import followit
followit.register(Car)
followit.register(Alligator)
followit.register(get_user_model())#to test following users
