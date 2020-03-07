from app import create_app as wikisearch_create_app
from flask_testing import TestCase


class BaseTest(TestCase):

    def create_app(self):
        app = wikisearch_create_app()
        return app


class TestAPI(BaseTest):

    def test_search_get(self):
        response = self.client.get("/api/search")
        self.assertEqual(response.status_code , 200)
        self.assertEquals(response.json, {'search': 'Hello API'})