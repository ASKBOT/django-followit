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

Copyright 2011 Evgeny Fadeev evgeny.fadeev@gmail.com
The source code is available under BSD license.
"""
REGISTRY = {}

def get_model_name(model):
    return model._meta.module_name


def get_bridge_class_name(model):
    return 'Follow' + get_model_name(model)


def get_model(model_name):
    """gets model from the current app"""
    from django.db import models as django_models
    return django_models.get_model('followit', model_name)


def get_bridge_model_for_object(obj):
    """returns bridge model used to follow items
    like the ``obj``
    """
    bridge_model_name = get_bridge_class_name(obj.__class__)
    return get_model(bridge_model_name)

def get_object_followers(obj):
    """returns query set of users following the object"""
    bridge_lookup_field = get_bridge_class_name(obj.__class__).lower()
    obj_model_name = get_model_name(obj.__class__)
    filter_criterion = 'followed_' + obj_model_name + '_records__object'
    filter = {filter_criterion: obj}
    from django.contrib.auth.models import User
    return User.objects.filter(**filter)


def make_followed_objects_getter(model):
    """returns query set of objects of a class ``model``
    that are followed by a user"""

    #something like followX_set__user
    def followed_objects_getter(user):
        filter = {'follower_records__user': user}
        return model.objects.filter(**filter)

    return followed_objects_getter

def test_follow_method(user, obj):
    """True if object ``obj`` is followed by the user,
    false otherwise, no error checking on whether the model
    has or has not been registered with the ``followit`` app
    """
    bridge_model = get_bridge_model_for_object(obj)
    try:
        #in django 1.2 there is method ``exists()``
        bridge_model.objects.get(user = user, object = obj)
        return True
    except bridge_model.DoesNotExist:
        return False


def make_follow_method(model):
    """returns a method that adds a FollowX record
    for an object
    """
    def follow_method(user, obj):
        """returns ``True`` if follow operation created a new record"""
        bridge_model = get_bridge_model_for_object(obj)
        bridge, created = bridge_model.objects.get_or_create(
                                                    user = user,
                                                    object = obj)
        return created
    return follow_method


def make_unfollow_method(model):
    """returns a method that allows to unfollow an item
    """
    def unfollow_method(user, obj):
        """attempts to find an item and delete it, no
        exstence checking
        """
        bridge_model = get_bridge_model_for_object(obj)
        objects = bridge_model.objects.get(user = user, object = obj)
        objects.delete()
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
    from django.contrib.auth.models import User

    model_name = get_model_name(model)
    if model in REGISTRY:
        return
    REGISTRY[model_name] = model

    #1) - create a new class FollowX
    class Meta(object):
        app_label = 'followit'

    fields = {
        'user': ForeignKey(
                        User,
                        related_name = 'followed_' + model_name + '_records'
                    ),
        'object': ForeignKey(
                                model,
                                related_name = 'follower_records'
                            ),
        '__module__': followit_models.__name__,
        'Meta': Meta
    }


    #create the bridge model class
    bridge_class_name = get_bridge_class_name(model)
    bridge_model = type(bridge_class_name, (django_models.Model,), fields)
    setattr(followit_models, bridge_class_name, bridge_model)

    #2) patch ``model`` with method ``get_followers()``
    model.add_to_class('get_followers', get_object_followers)

    #3) patch ``User`` with method ``get_followed_Xs``
    method_name = 'get_followed_' + model_name + 's'
    getter_method = make_followed_objects_getter(model)
    User.add_to_class(method_name, getter_method)

    #4) patch ``User with method ``is_following()``
    if not hasattr(User, 'is_following'):
        User.add_to_class('is_following', test_follow_method)

    #5) patch ``User`` with method ``follow_X``
    follow_method = make_follow_method(model)
    User.add_to_class('follow_' + model_name, follow_method)

    #6) patch ``User`` with method ``unfollow_X``
    unfollow_method = make_unfollow_method(model)
    User.add_to_class('unfollow_' + model_name, unfollow_method)
