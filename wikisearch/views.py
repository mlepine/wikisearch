from flask import (
    jsonify, Blueprint, render_template, current_app as app, request, abort
)
from wikisearch.search import search_index


wikisearch = Blueprint('wikisearch', __name__)


@wikisearch.route('/')
def index():
    q = request.args.get('q') or ''
    docs = []
    if q:
        app.logger.info(f'Searching for "{q}"')
        docs = search_index.search(q)
        app.logger.info(f'Found {len(docs)} results')
    return render_template('index.html', q=q, count=len(docs), docs=docs)


@wikisearch.route('/api/search')
def search():
    q = request.args.get('q')
    if q:
        app.logger.info(f'Searching for "{q}"')
        docs = search_index.search(q)
        app.logger.info(f'Found {len(docs)} results')
        return jsonify({'results': docs, 'count': len(docs)})
    return jsonify([])


@wikisearch.route('/api/docs')
def list_docs():
    return jsonify(search_index._docs)


@wikisearch.route('/api/docs/<int:doc_id>')
def get_doc(doc_id):
    try:
        return jsonify(search_index._docs[doc_id])
    except IndexError:
        abort(404)


@wikisearch.route('/api/index')
def index_stats():
    return jsonify({
        'documents_count': len(search_index._docs),
        'terms_count': len(search_index._index),
        'top_terms': sorted(
            ([term, len(docs)] for term, docs in search_index._index.items()),
            reverse=True, key=lambda x: x[1]
        )[:20]
    })
