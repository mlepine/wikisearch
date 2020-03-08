from flask import Flask
from wikisearch.views import wikisearch
from wikisearch.search import initialize_search

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
