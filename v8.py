import logging.config
import time
import uuid
from functools import wraps

from flask import Flask, g
from flask.views import MethodView

from common import get_logging_config


logging.config.dictConfig(get_logging_config(['context']))


def global_error_handler(e):
    app.logger.error(str(e), exc_info=e)
    return 'unexpected error', 500


def add_request_id():
    def decorator(f):
        @wraps(f)
        def decorated_function(self):
            request_id = uuid.uuid4()
            g.log_context = {
                'request_id': request_id,
                'view': self.__class__.__name__,
            }

            app.logger.info(f'hello from middleware ({request_id})')
            return f(self, request_id)
        return decorated_function
    return decorator


class HelloView(MethodView):
    @add_request_id()
    def get(self, request_id):
        time.sleep(0.01)
        app.logger.info(f'hello from view ({request_id})')
        raise Exception('oops')


app = Flask(__name__)
app.add_url_rule('/', view_func=HelloView.as_view('hello'))
app.register_error_handler(404, lambda _: ('', 404))
app.register_error_handler(Exception, global_error_handler)

if __name__ == '__main__':
    app.run()
