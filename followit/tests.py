"""
Test cases for the follower module
"""
from django.db import models, transaction
from django.contrib.contenttypes.management import update_contenttypes
from django.core.management.commands import syncdb
from django.test import TestCase

import follower

class SomeJunk(models.Model):
    yeah = models.BooleanField(default = True)

class SomeTrash(models.Model):
    yeah = models.BooleanField(default = True)

class FollowerTests(TestCase):
    """idea taken from Dan Rosemans blog
    http://blog.roseman.org.uk/2010/04/13/temporary-models-django/
    create a temp model in setUp(), run tests on it, then destroy it in dearDown()
    """

    def setUp(self):
        models.register_models('followertests', SomeJunk)
        models.signals.post_syncdb.disconnect(update_contenttypes)

    def test_register_fk_follow(self):
        follower.register(SomeJunk)
        #call_command('syncdb')
        cmd = syncdb.Command()#south messes up here - call django's command directly
        cmd.execute()
        transaction.commit()
        #test that table `follower_followsomejunk` exists
        model = models.get_model('follower', 'FollowSomeJunk')
        self.assertEquals(model.objects.count(), 0)

    #def tearDown(self):
    #    cursor = connection.cursor()
    #    cursor.execute('DROP TABLE `followertests_somejunk`')
