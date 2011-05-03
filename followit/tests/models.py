from django.db import models

class SomeJunk(models.Model):
    yeah = models.BooleanField(default = True)

class SomeTrash(models.Model):
    yeah = models.BooleanField(default = True)

import followit
followit.register(SomeJunk)
followit.register(SomeTrash)

