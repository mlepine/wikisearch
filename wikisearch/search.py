import requests
import random
import nltk
from flask import g
from werkzeug.local import LocalProxy
from itertools import chain, groupby
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer


API_URL = 'https://en.wikipedia.org/w/api.php'


def search_articles():
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': 'startups',
        'srlimit': 100
    }
    resp = requests.get(API_URL, params=params).json()
    return resp['query']['search']


def fetch_article(pageid):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'formatversion': 2,
        'pageids': pageid,
        'exlimit': 1,
        'explaintext': 1
    }
    resp = requests.get(API_URL, params=params).json()
    return resp['query']['pages'][0]


def fetch_articles():
    results = search_articles()
    # Randomly choose 10 articles
    results = random.sample(results, 10)
    articles = [fetch_article(r['pageid']) for r in results]
    return articles


class SearchIndex:

    def __init__(self):
        self._index = defaultdict(list)
        self._docs = []
        self.stemmer = EnglishStemmer()
        self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def tokenize(self, text):
        text = text.lower()
        # Tokenenize text and filter punctuation and stopwords
        return (
            self.stemmer.stem(token)
            for token in nltk.word_tokenize(text)
            if token.isalpha() and token not in self.stopwords
        )

    def add_doc(self, doc, text_fn=None):
        if not text_fn:
            def text_fn(x): return x
        text = text_fn(doc)
        tokens = list(self.tokenize(text))
        termfreq = sorted((
            [len(list(it)), token]
            for token, it in groupby(sorted(tokens))
        ), reverse=True)
        doc = {
            'id': len(self._docs),
            'termfreq': termfreq,
            'tokens': tokens,
            'doc': doc
        }
        self._docs.append(doc)
        for i, token in enumerate(tokens):
            token = self.stemmer.stem(token)
            self._index[token].append((i, doc))

    def search(self, q):
        q = self.tokenize(q)
        results = (self._index.get(token) or [] for token in q)
        results = sorted(
            (doc['id'], len(docs), position)
            for docs in results for position, doc in docs
        )
        # Group results by id
        results = groupby(results, key=lambda x: x[0])

        ret = []
        for id, results in results:
            doc = self._docs[id]
            # Score based on number of matching docs and how rare the token is
            score = sum(1/(freq + position) for _, freq, position in results)
            ret.append({'doc': doc, 'score': score})

        return sorted(ret, key=lambda doc: doc['score'], reverse=True)


def initialize_search():
    articles = fetch_articles()
    idx = SearchIndex()
    for article in articles:
        idx.add_doc(article, lambda x: x['extract'])
    return idx


_search_index = None


def get_search_index():
    global _search_index
    if _search_index is None:
        _search_index = initialize_search()

    return _search_index


search_index = LocalProxy(get_search_index)