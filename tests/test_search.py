from unittest import TestCase
from wikisearch.search import SearchIndex


class TestSearchIndex(TestCase):

    def test_add_doc(self):
        idx = SearchIndex()
        doc = 'The quick brown fox jumped over the fence.'
        idx.add_doc({'text': doc})
        results = idx.search('fox')
        self.assertEqual(round(results[0]['score'], 3), 0.333)
        self.assertEqual(results[0]['doc']['text'], doc)
        self.assertEqual(results[0]['doc']['termfreq'], [
            [1, 'quick'],
            [1, 'jump'],
            [1, 'fox'],
            [1, 'fenc'],
            [1, 'brown'],
        ])
