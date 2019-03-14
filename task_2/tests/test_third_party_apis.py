import json
import unittest

from app import create_app, db
from app.models import Subscriber, Subscription
from app.tasks import get_ticker

class AlphavantageAPITestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')

		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_valid_ticker(self):
		data = get_ticker('^GSPC')
		self.assertIsNotNone(data)

	def test_invalid_ticker(self):
		data = get_ticker('AAAA')
		self.assertIsNone(data)
