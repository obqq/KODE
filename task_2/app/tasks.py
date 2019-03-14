import json
import time
import requests

from flask import current_app, url_for
from app.models import Subscriber, Subscription
from app.email import send_notification



def test_scheduler(app):
	app.logger.info('Running background task')


def get_ticker(ticker_name):
	app = current_app._get_current_object()
	API_KEY = app.config["AV_API_KEY"]
	url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE' \
		  f'&symbol={ticker_name}&apikey={API_KEY}'

	attempts = 0
	while attempts < 3:
		try:
			response = requests.get(url)

			if response.ok:
				json_data = response.json()

				data = json_data.get('Global Quote')
				if data == {}:
					data = None
				return data
			else:
				attempts += 1
				time.sleep(1)
				continue
		except requests.exceptions.RequestException as e:
			app.logger.error(e)


	if attempts == 3:
		error = 'Looks like API limit has been reached.'

		app.logger.error(error)
		return None



def update_tickers(app):
	with app.app_context():
		followed_tickers = {}
		for subscription in Subscription.query.distinct(Subscription.ticker_name):
			ticker_name = subscription.ticker_name
			if ticker_name not in followed_tickers.keys():
				data = get_ticker(ticker_name)

				if data is not None:
					followed_tickers.update({ticker_name: float(data['05. price'])})


		subscriptions = Subscription.query
		for subscription in subscriptions:
			ticker_name = subscription.ticker_name
			ticker_price = followed_tickers.get(ticker_name)

			if ticker_price is not None:
				if subscription.max_price is not None and subscription.max_price < ticker_price:
					message = f'''Price of {ticker_name} ticker has soared higher than {subscription.max_price}.\n
							  Is is currently trading at {ticker_price}.'''
				elif subscription.min_price is not None and ticker_price > subscription.min_price:
					message = f'''Price of {ticker_name} ticker has fallen below {subscription.min_price}.\n
							  Is is currently trading at {ticker_price}.'''
				else:
					continue

				subscriber = Subscriber.query.filter_by(id=subscription.subscriber_id).first()

				send_notification(subscriber.email, message)
