import logging.config
import time
import uuid
from functools import wraps

from flask import Flask
from flask.views import MethodView

from common import get_logging_config

logging.config.dictConfig(get_logging_config())


class ContextLogger:
    def __init__(self, logger):
        self.__logger = logger
        self.__context = {}

    def add_context(self, key, value):
        self.__context[key] = value

    def info(self, message):
        self.__logger.info(message, extra=self.__context)


def add_request_id(logger):
    def decorator(f):
        @wraps(f)
        def decorated_function(self):
            request_id = uuid.uuid4()
            logger.add_context('request_id', request_id)
            logger.info(f'hello from middleware ({request_id})')
            return f(self, request_id)
        return decorated_function
    return decorator


class HelloView(MethodView):
    logger = ContextLogger(logging.getLogger('view.hello'))

    @add_request_id(logger)
    def get(self, request_id):
        time.sleep(0.01)
        self.logger.info(f'hello from view ({request_id})')
        return 'Hello World'


app = Flask(__name__)
app.add_url_rule('/', view_func=HelloView.as_view('hello'))

if __name__ == '__main__':
    app.run()
