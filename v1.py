import logging.config

from flask import Flask
from flask.views import MethodView

from common import get_logging_config

logging.config.dictConfig(get_logging_config())


class HelloView(MethodView):
    logger = logging.getLogger('view.hello')

    def get(self):
        self.logger.info('hello from view')
        return 'Hello World\n'


app = Flask(__name__)
app.add_url_rule('/', view_func=HelloView.as_view('hello'))

if __name__ == '__main__':
    app.run()
