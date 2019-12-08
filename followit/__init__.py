"""A Django App allowing :class:`~django.contrib.auth.models.User` to 
follow instances of any other django models, including other users

To use this module:
* add "followit" to the ``INSTALLED_APPS`` in your ``settings.py``
* in your app's ``models.py`` add:

    import followit
    followit.register(Thing)

* run ``python manage.py syncdb``
* then anywhere in your code you can do the following:

    user.follow(some_thing_instance)
    user.unfollow(some_thing_instance)

    user.get_followed_things() #note that "things" is from the name of class Thing
    some_thing.get_followers()

Copyright 2011-2019 Evgeny Fadeev evgeny.fadeev@gmail.com
The source code is available under BSD license.
"""
import django
import sys
from django.core.exceptions import ImproperlyConfigured

if django.VERSION[:2] == (1, 7) and sys.version_info.major == 3:
    msg = """\n\nThis version of django-followit does not Django 1.7 with Python 3
Either use Python 2.7 or upgrade Django to version from 1.8 up to 3.
"""
    raise ImproperlyConfigured(msg)

if django.VERSION < (1, 7) or django.VERSION >= (4, 0):
    msg = "\n\nThis version of django-followit supports Django 1.7 - 3."

    if django.VERSION < (1, 7):
        msg += "\nFor earlier Django versions try django-followit 0.0.9"

    raise ImproperlyConfigured(msg)

from followit import utils
from followit.compat import get_user_model

REGISTRY = {}


def get_model_name(model):
    try:
        return model._meta.module_name
    except AttributeError:
        return model._meta.model_name


def get_follow_records(user, obj):
    from django.contrib.contenttypes.models import ContentType
    from followit.models import FollowRecord
    ct = ContentType.objects.get_for_model(obj)
    return FollowRecord.objects.filter(
                                content_type=ct,
                                object_id=obj.pk,
                                user=user
                            )


def get_object_followers(obj):
    """returns query set of users following the object"""
    from django.contrib.contenttypes.models import ContentType
    from followit.models import FollowRecord
    ct = ContentType.objects.get_for_model(obj)
    fr_set = FollowRecord.objects.filter(content_type=ct, object_id=obj.pk)
    uids = fr_set.values_list('user', flat=True)
    User = get_user_model()
    return User.objects.filter(pk__in=uids)


def make_followed_objects_getter(model):
    """returns query set of objects of a class ``model``
    that are followed by a user"""

    #something like followX_set__user
    def followed_objects_getter(user):
        from followit.models import FollowRecord
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(model)
        fr_set = FollowRecord.objects.filter(
                                content_type=ct,
                                user=user
                            )
        obj_id_set = fr_set.values_list('object_id', flat=True)
        return model.objects.filter(pk__in=obj_id_set)


    return followed_objects_getter

def test_follow_method(user, obj):
    """True if object ``obj`` is followed by the user,
    false otherwise, no error checking on whether the model
    has or has not been registered with the ``followit`` app
    """
    fr_set = get_follow_records(user, obj)
    return fr_set.exists()


def make_follow_method(model):
    """returns a method that adds a FollowX record
    for an object
    """
    def follow_method(user, obj):
        """returns ``True`` if follow operation created a new record"""
        from followit.models import FollowRecord
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(obj)
        fr, created = FollowRecord.objects.get_or_create(
                                                    content_type=ct,
                                                    object_id=obj.pk,
                                                    user=user
                                                )
        return created
    return follow_method


def make_unfollow_method(model):
    """returns a method that allows to unfollow an item
    """
    def unfollow_method(user, obj):
        """attempts to find an item and delete it, no
        exstence checking
        """
        fr_set = get_follow_records(user, obj)
        fr_set.delete()
    return unfollow_method


def register(model):
    """returns model class that connects
    User with the followed object

    ``model`` - is the model class to follow

    The ``model`` class gets new method - ``get_followers``
    and the User class - a method - ``get_followed_Xs``, where
    the ``X`` is the name of the model
    and ``is_following(something)``
    
    Note, that proper pluralization of the model name is not supported,
    just "s" is added
    """
    from followit import models as followit_models
    from django.db import models as django_models
    from django.db.models.fields.related import ForeignKey

    User = get_user_model()

    model_name = get_model_name(model)
    if model in REGISTRY:
        return
    REGISTRY[model_name] = model

    #1) patch ``model`` with method ``get_followers()``
    model.add_to_class('get_followers', get_object_followers)

    #2) patch ``User`` with method ``get_followed_Xs``
    method_name = 'get_followed_' + model_name + 's'
    getter_method = make_followed_objects_getter(model)
    User.add_to_class(method_name, getter_method)

    #3) patch ``User with method ``is_following()``
    if not hasattr(User, 'is_following'):
        User.add_to_class('is_following', test_follow_method)

    #4) patch ``User`` with method ``follow_X``
    follow_method = make_follow_method(model)
    User.add_to_class('follow_' + model_name, follow_method)

    #5) patch ``User`` with method ``unfollow_X``
    unfollow_method = make_unfollow_method(model)
    User.add_to_class('unfollow_' + model_name, unfollow_method)
