"""Views for the ``followit`` app,
all are ajax views and return application/json mimetype
"""
from followit import utils

@utils.followit_ajax_view
@utils.post_only
def follow_object(request, model_name = None, object_id = None):
    """follows an object and returns status:
    * 'success' - if an object was successfully followed
    * 'noop' - if the same object was followed before by the same user
    * the decorator takes care of the error situations
    """

    obj = utils.get_object(model_name, object_id)
    follow_func = getattr(request.user, 'follow_' + model_name)
    created = follow_func(obj)
    if created:
        return {'status': 'success'}
    else:
        return {'status': 'noop'}


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
