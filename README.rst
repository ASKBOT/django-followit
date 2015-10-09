.. image:: https://travis-ci.org/vinodpandey/django-followit.png?branch=master
    :alt: Build Status
    :align: left

The ``followit`` django app allows to easily set up a
capability for the site users to follow various things on the site,
represented by django model ``followit.models.FollowRecord`` 
using the ``django.contrib.models.ContentTypes`` system.

Release Notes
=============
Starting the version ``0.0.8`` it is not necessary to run ``syncdb`` for this app,
but instead run the ``migrate`` command.


Setup
========

To the INSTALLED_APPS in your ``settings.py`` add entry ``'followit'``.
Then, in your apps' ``models.py``, probably at the end of the file, add::
    import followit
    followit.register(Thing)

Once that is done, in your shell run::
    python manage.py migrate followit

Not it will be possible for the user to follow instances of ``SomeModel``.

If you decide to allow following another model, just add another
``followit.register(...)`` statement to the ``models.py``.

Usage
============

Examples below show how to use ``followit`` (assuming that model ``Thing``
is registered with ``followit`` in your ``models.py``::
    bob.follow_thing(x)
    bob.unfollow_thing(x)
    things = bob.get_followed_things()
    x_followers = x.get_followers()

Available urls from the `followit/urls.py`::
    /follow/<model_name>/<item_id>/

    {% url follow_object "somemodel" item_id %} #model name lower case

    /unfollow/<model_name>/<item_id>/

    {% url unfollow_object "somemodel" item_id %} #lower case model name

    /toggle-follow/<model_name>/<item_id>/

    {% url toggle_follow_object "somemodel" item_id %} #lower case model name

``followit`` does not yet provide template tags.
