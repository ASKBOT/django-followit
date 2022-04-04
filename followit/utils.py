"""utility functions used by the :mod:`followit`
"""
import functools
import json
from django.http import HttpResponse
import followit

def get_object(model_name, object_id):
    """not a view, just a function, returning an object"""
    model = followit.REGISTRY[model_name]
    return model.objects.get(id = object_id)

def del_related_objects_cache(model):
    try:
        del model._meta._related_objects_cache
    except AttributeError:
        pass
    try:
        del model._meta._related_objects_proxy_cache
    except AttributeError:
        pass

def followit_ajax_view(view_func):
    """decorator that does certain error checks on the input
    and serializes response as json

    in the case of error, json output will contain
    """
    @functools.wraps(view_func)
    def wrapped_view(request, model_name = None, object_id = None):
        try:
            assert(model_name in followit.REGISTRY)
            assert(request.user.is_authenticated)
            assert(request.method == 'POST')
            assert(request.is_ajax())
            data = view_func(request, model_name, object_id)
        except Exception as e:
            data = {'status': 'error', 'error_message': str(e)}

        return HttpResponse(json.dumps(data), content_type='application/json')
    return wrapped_view

def post_only(view_func):
    """simple decorator raising assertion error when method is not 'POST"""
    @functools.wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        assert(request.method == 'POST')
        return view_func(request, *args, **kwargs)
    return wrapped_view
 
