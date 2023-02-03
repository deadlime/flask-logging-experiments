import logging.config
import uuid

from flask import Flask, g, request
from flask.views import MethodView

from common import get_logging_config


logging.config.dictConfig(get_logging_config(['context']))


class HelloView(MethodView):
    def get(self):
        g.log_context['view'] = self.__class__.__name__

        app.logger.info(f'hello from view')
        raise Exception('oops')


app = Flask(__name__)
app.add_url_rule('/', view_func=HelloView.as_view('hello'))


@app.before_request
def init_logging_context():
    g.log_context = {
        'request_id': uuid.uuid4(),
        'ip': request.remote_addr,
    }


@app.errorhandler(404)
def not_found_handler(_):
    return 'not found', 404


@app.errorhandler(Exception)
def global_error_handler(e):
    app.logger.error(str(e), exc_info=e)
    return 'unexpected error', 500


if __name__ == '__main__':
    app.run()
