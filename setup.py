from setuptools import setup, find_packages
import ez_setup
ez_setup.use_setuptools()

setup(
    name="django-followit",
    version='0.4.0',
    description='A Django application that allows users to follow django model objects',
    packages=find_packages(),
    author='Evgeny.Fadeev',
    author_email='evgeny.fadeev@gmail.com',
    license='BSD License',
    keywords='follow, database, django',
    url='https://github.com/ASKBOT/django-followit',
    include_package_data=True,
    install_requires=['simplejson',],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    long_description="""The ``followit`` django app allows to easily set up a
capability for the site users to follow various things on the site,
represented by django model ``followit.models.FollowRecord`` 
using the ``django.contrib.models.ContentTypes`` system.

Release Notes
=============

Django version support is encoded in the version of the package.
For a given version of Django first two digits will not change.
The last digits indicates the bugfix releases. Below the .x
in the version should be replaced with the highest available digit::

  * ``0.4.x`` support django versions 2 and 3, only Python 3.
  * ``0.3.x`` - django 1.9 - 1.11
  * ``0.2.x`` - django 1.8
  * ``0.1.x`` - django 1.7
  * ``0.0.9`` can be used for the earlier versions

Starting the version 0.1.0 , method `register` must be called from your app's
`AppConfig.ready()` method.

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

Available urls from the `followit/urls.py`::
    /follow/<model_name>/<item_id>/
    {% url follow_object "somemodel" item_id %} #model name lower case

    /unfollow/<model_name>/<item_id>/
    {% url unfollow_object "somemodel" item_id %} #lower case model name

    /toggle-follow/<model_name>/<item_id>/
    {% url toggle_follow_object "somemodel" item_id %} #lower case model name


``followit`` does not yet provide template tags.
"""
)
