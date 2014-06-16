from functools import wraps

from flask import request, current_app, Response


def jsonp(f):
    '''Wraps JSONified output for JSONP.
    wrapped function must return str or unicode.
    '''

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback')
        if callback:
            json_content = f(*args, **kwargs)
            js_expression = u'{0}({1})'.format(callback, json_content)
            return current_app.response_class(js_expression, mimetype='application/javascript; charset=utf-8')
        else:
            return Response(f(*args, **kwargs), mimetype='application/json; charset=utf-8')

    return decorated_function
