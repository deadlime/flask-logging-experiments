import logging.config
import time
import uuid
from functools import wraps

from flask import Flask, g
from flask.views import MethodView

from common import get_logging_config

logging.config.dictConfig(get_logging_config())


class GContextLogger:
    def __init__(self, logger):
        self.__logger = logger

    def info(self, message):
        self.__logger.info(message, extra=g.log_context)


def add_request_id(logger):
    def decorator(f):
        @wraps(f)
        def decorated_function(self):
            request_id = uuid.uuid4()
            g.log_context = {'request_id': request_id}

            logger.info(f'hello from middleware ({request_id})')
            return f(self, request_id)
        return decorated_function
    return decorator


class HelloView(MethodView):
    logger = GContextLogger(logging.getLogger('view.hello'))

    @add_request_id(logger)
    def get(self, request_id):
        time.sleep(0.01)
        self.logger.info(f'hello from view ({request_id})')
        return 'Hello World'


app = Flask(__name__)
app.add_url_rule('/', view_func=HelloView.as_view('hello'))

if __name__ == '__main__':
    app.run()
