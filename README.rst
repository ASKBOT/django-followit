.. image:: https://travis-ci.org/vinodpandey/django-followit.png?branch=master
        :alt: Build Status
        :align: left

The ``followit`` django app allows for the site users
to follow various instances of Django models,
represented by django model ``followit.models.FollowRecord`` 
using the ``django.contrib.models.ContentTypes`` system.

Release Notes
=============

The list below shows compatibility of `django-followit` with versions of Django and Python.
Python version compatibility was thoroughly tested only with release `0.4.0`::

  * ``0.5.x`` supports django versions 1.10 and up.
  * ``0.4.x`` django 1.7(**) - 1.9. Python 2 and 3.
  * ``0.3.x`` - django 1.9 - 1.11
  * ``0.2.x`` - django 1.8
  * ``0.1.x`` - django 1.7
  * ``0.0.9`` can be used for the earlier versions

(**) versions ``0.4.x`` do not support Django 1.7 with Python 3.

Setup
=====

To the INSTALLED_APPS in your ``settings.py`` add entry ``'followit'``.

Run `python manage.py migrate followit`

Then, in the body of `AppConfig.ready` method, add::

    import followit
    followit.register(Thing)

Not it will be possible for the user to follow instances of ``SomeModel``.

If you decide to allow following another model, just add another
``followit.register(...)`` statement.

Usage
=====

Examples below show how to use ``followit``::

    bob.follow_thing(x)
    bob.unfollow_thing(x)
    things = bob.get_followed_things()
    x_followers = x.get_followers()

To follow/unfollow items via the HTTTP, make AJAX post requests at urls,
available urls ``followit/urls.py``::

    /follow/<model_name>/<item_id>/
    {% url follow_object "somemodel" item_id %} #model name lower case

    /unfollow/<model_name>/<item_id>/
    {% url unfollow_object "somemodel" item_id %} #lower case model name

    /toggle-follow/<model_name>/<item_id>/
    {% url toggle_follow_object "somemodel" item_id %} #lower case model name
