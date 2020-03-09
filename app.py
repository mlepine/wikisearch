import logging
from flask import Flask
from flask.logging import default_handler
from wikisearch.views import wikisearch
from wikisearch.search import initialize_search

root_logger = logging.getLogger()
root_logger.addHandler(default_handler)


CONFIGS = {
    'production': 'config.ProdConfig',
    'testing': 'config.TestConfig',
    'development': 'config.DevConfig'
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(CONFIGS.get(app.env))
    app.register_blueprint(wikisearch)
    return app
