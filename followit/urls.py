from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(
        r'^follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        'followit.views.follow_object',
        name = 'follow_object'
    ),
    url(
        r'^unfollow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        'followit.views.unfollow_object',
        name = 'unfollow_object'
    )
)
