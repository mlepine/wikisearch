from flask import jsonify
from flask import Blueprint, render_template
from flask import current_app as app


wikisearch = Blueprint('wikisearch', __name__)


@wikisearch.route('/')
def index():
    app.logger.info('Loading index.html')
    return render_template('index.html')


@wikisearch.route('/api/search')
def search():
    return  jsonify({'search': 'Hello API'})