"""Views for the ``followit`` app,
all are ajax views and return application/json mimetype
"""
from followit import utils

@utils.followit_ajax_view
@utils.post_only
def follow_object(request, model_name = None, object_id = None):
    """follows an object and returns status:
    * 'success' - if an object was successfully followed
    * the decorator takes care of the error situations
    """
    obj = utils.get_object(model_name, object_id)
    follow_func = getattr(request.user, 'follow_' + model_name)
    follow_func(obj)
    return {'status': 'success'}


@utils.followit_ajax_view
@utils.post_only
def unfollow_object(request, model_name = None, object_id = None):
    """unfollows an object and returns status 'success' or
    'error' - via the decorator :func:`~followit.utils.followit_ajax_view`
    """
    obj = utils.get_object(model_name, object_id)
    unfollow_func = getattr(request.user, 'unfollow_' + model_name)
    unfollow_func(obj)
    return {'status': 'success'}


@utils.followit_ajax_view
@utils.post_only
def toggle_follow_object(request, model_name = None, object_id = None):
    """if object is followed then unfollows
    otherwise follows

    returns json
    {
        'status': 'success', # or 'error'
        'following': True, #or False
    }

    
    unfollows an object and returns status 'success' or
    'error' - via the decorator :func:`~followit.utils.followit_ajax_view`
    """
    obj = utils.get_object(model_name, object_id)
    if request.user.is_following(obj):
        toggle_func = getattr(request.user, 'unfollow_' + model_name)
        following = False
    else:
        toggle_func = getattr(request.user, 'follow_' + model_name)
        following = True

    toggle_func(obj)
    return {
        'status': 'success',
        'following': following
    }
