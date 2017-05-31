import json
import unittest

from setgame import SetBoard, SetDeck
import web.app

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = web.app.app.test_client()

    def test_empty_boards_at_startup(self):
        res = self.app.get('/api/boards')
        self.assertEqual([], json.loads(res.data))