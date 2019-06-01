from functools import wraps
from flask import request, abort
import os
from wordweaver.config import ENV_CONFIG

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if ENV_CONFIG['api_key']:
            if 'x-api-key' in request.headers and request.headers['x-api-key'] == ENV_CONFIG['api_key']:
                return view_function(*args, **kwargs)
            else:
                abort(403)
        else:
            return view_function(*args, **kwargs)

    return decorated_function