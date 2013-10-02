"""utility functions used by the :mod:`followit`
"""
import functools
from django.utils import simplejson
from django.http import HttpResponse
import followit

def get_object(model_name, object_id):
    """not a view, just a function, returning an object"""
    model = followit.REGISTRY[model_name]
    return model.objects.get(id = object_id)

def followit_ajax_view(view_func):
    """decorator that does certain error checks on the input
    and serializes response as json

    in the case of error, json output will contain
    """
    @functools.wraps(view_func)
    def wrapped_view(request, model_name = None, object_id = None):
        try:
            assert(model_name in followit.REGISTRY)
            assert(request.user.is_authenticated())
            assert(request.method == 'POST')
            assert(request.is_ajax())
            data = view_func(request, model_name, object_id)
        except Exception, e:
            data = {'status': 'error', 'error_message': unicode(e)}

        return HttpResponse(simplejson.dumps(data), mimetype = 'application/json')
    return wrapped_view

def post_only(view_func):
    """simple decorator raising assertion error when method is not 'POST"""
    @functools.wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        assert(request.method == 'POST')
        return view_func(request, *args, **kwargs)
    return wrapped_view

def get_user_model():
    """version-independent function "get_user_model" """
    try:
        from django.contrib.auth import get_user_model
    except ImportError: # django < 1.5
        from django.contrib.auth.models import User
    else:
        User = get_user_model()
    return User    
