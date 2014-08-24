from django.db import models
from followit.compat import User

class Car(models.Model):
    yeah = models.BooleanField(default = True)

class Alligator(models.Model):
    yeah = models.BooleanField(default = True)

import followit
followit.register(Car)
followit.register(Alligator)
followit.register(User)#to test following users
