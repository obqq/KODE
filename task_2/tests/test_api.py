import json
import unittest

from app import create_app, db
from app.models import Subscriber, Subscription
from app.tasks import get_ticker


class APITestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')

		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_get_method(self):
		response = self.client.get('/api/subscription',
								   content_type='application/json')

		self.assertEqual(response.status_code, 405)

	def test_post_method(self):
		response = self.client.post('/api/subscription',
									content_type='application/json')

		self.assertEqual(response.status_code, 400)

	def test_invalid_json(self):
		data = {'ticker': 'AAAA',
				'email': 'test_user@gmail.com'}

		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')

		self.assertEqual(response.status_code, 400)

		data = {'ticker': 'AAAA',
				'email': 'test_user@gmail.com',
				'max_price': '123',
				'min_price': 142}

		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')

		self.assertEqual(response.status_code, 400)

	def test_valid_json(self):
		data = {'ticker': 'AAAA',
				'email': 'test_user@gmail.com',
				'max_price': 123,
				'min_price': 142}

		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')

		self.assertEqual(response.status_code, 200)

	def test_same_tickers(self):
		data = {'ticker': 'AAAA',
				'email': 'test_user@gmail.com',
				'max_price': 123,
				'min_price': 142}

		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')
		self.assertEqual(response.json.get('error'), {})

		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')
		self.assertNotEqual(response.json.get('error'), {})

	def test_six_tickers(self):
		data = {'ticker': '',
				'email': 'test_user@gmail.com',
				'max_price': 123,
				'min_price': 142}

		for i in range(5):
			data['ticker'] = f'AAA{i}'

			response = self.client.post('/api/subscription', data=json.dumps(data),
										content_type='application/json')
			self.assertEqual(response.json.get('error'), {})

		data['ticker'] = 'AAA5'
		response = self.client.post('/api/subscription', data=json.dumps(data),
									content_type='application/json')
		self.assertNotEqual(response.json.get('error'), {})
