from logging import Filter

from flask import has_request_context, g


class LogContextFilter(Filter):
    def filter(self, record):
        if has_request_context() and hasattr(g, 'log_context'):
            for k, v in g.log_context.items():
                setattr(record, k, v)

        return True


def get_logging_config(filters=None):
    return {
        'version': 1,
        'formatters': {
            'json': {
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(name)s %(message)s'
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'json',
                'filters': filters,
                'level': 'INFO',
            },
        },
        'filters': {
            'context': {
                '()': 'common.LogContextFilter',
            }
        },
        'root': {
            'level': 'INFO',
            'propagate': True,
            'handlers': ['wsgi'],
        },
    }
