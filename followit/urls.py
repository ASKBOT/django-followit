from django.conf.urls import url

from . import views as FollowitViews

urlpatterns = [
    url(
        r'^follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.follow_object,
        name = 'follow_object'
    ),
    url(
        r'^unfollow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.unfollow_object,
        name = 'unfollow_object'
    ),
    url(
        r'^toggle-follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        FollowitViews.toggle_follow_object,
        name='toggle_follow_object'
    )
]
