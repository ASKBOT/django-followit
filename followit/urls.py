from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^follow/(?P<model>\w+)/(?P<id>\d+)/$',
        'followit.views.follow',
        name = 'follow_object'
    ),
    url(
        r'^unfollow/(?P<model>\w+)/(?P<id>\d+)/$',
        'followit.views.unfollow',
        name = 'unfollow_object'
    )
)
