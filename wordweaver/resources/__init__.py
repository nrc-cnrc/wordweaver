from functools import wraps
from flask import request, abort
import os

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if os.environ.get('API_KEY'):
            if 'x-api-key' in request.headers and request.headers['x-api-key'] == os.environ.get('API_KEY'):
                return view_function(*args, **kwargs)
            else:
                abort(403)
        else:
            return view_function(*args, **kwargs)

    return decorated_function