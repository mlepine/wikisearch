import json
from app import create_app as wikisearch_create_app
from flask_testing import TestCase
from unittest.mock import patch


class BaseTest(TestCase):

    def create_app(self):
        app = wikisearch_create_app()
        return app


class TestAPI(BaseTest):

    def test_search_get(self):
        with patch('wikisearch.search.fetch_articles') as mock:
            with open('tests/data.json') as f:
                articles = json.load(f)
                mock.return_value = articles
            response = self.client.get('/api/search?q=startups')
            self.assertEqual(response.status_code, 200)
            results = response.json
            self.assertEquals(results['count'], 10)
            self.assertEquals(round(results['results'][0]['score'], 3), 0.093)
            self.assertEquals(
                results['results'][0]['doc']['title'], 'Macintosh startup'
            )
