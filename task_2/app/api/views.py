from flask import request, jsonify, url_for, redirect
from . import api
from .errors import bad_request, no_content
from .decorators import validate_json, validate_schema

from app import db
from app.models import Subscriber
from app.email import send_on_new_subscription


def ok_request(params, response):
	response = jsonify(
		{'error': {},
		 'params': params,
		 'response': response})
	response.status_code = 200
	return response


@api.route('/subscription', methods=['POST'])
@validate_json
@validate_schema('subscription_schema')
def new_subscription():
	email = request.json.get('email')
	ticker_name = request.json.get('ticker')
	max_price = request.json.get('max_price')
	min_price = request.json.get('min_price')

	if max_price is None and min_price is None:
		message = 'You haven\'t specified neither min_price nor max_price'
		return bad_request(request.json, message)

	if email == '':
		message = 'You haven\'t specified email'
		return bad_request(request.json, message)

	if ticker_name == '':
		message = 'You haven\'t specified ticker'
		return bad_request(request.json, message)

	subscriber = Subscriber.query.filter_by(email=email).first()

	if subscriber is None:
		subscriber = Subscriber(email=email)
		db.session.add(subscriber)
		db.session.flush()

		send_on_new_subscription(email, ticker_name)
		subscriber.subscribe(ticker_name, max_price, min_price)
		db.session.commit()

	elif subscriber.subscriptions.count() >= 5:
		message = 'You are subscribed to maximum number of tickers.'
		return bad_request(request.json, message)
	elif not subscriber.is_subscribed(ticker_name):
		subscriber.subscribe(ticker_name, max_price, min_price)
		db.session.commit()


		send_on_new_subscription(email, ticker_name)
	else:
		message = f'You are subscribed to {ticker_name} ticker already.'
		return bad_request(request.json, message)

	return ok_request(request.json, 1)


@api.route('/subscription', methods=['DELETE'])
def delete_subscription():
	email = request.args.get('email')
	ticker_name = request.args.get('ticker')

	params = {'email': email, 'ticker': ticker_name}

	if email is None:
		message = 'You haven\'t spesified any email to unsubscribe'
		return bad_request(params, message)

	subscriber = Subscriber.query.filter_by(email=email).first()

	if subscriber is None:
		message = 'You are not subscribed to any ticker yet.'
		return no_content(params, message)
	else:
		if ticker_name is None:
			for ticker in subscriber.subscriptions:
				subscriber.unsubscribe(ticker.ticker_name)

			db.session.commit()

			return ok_request(params, 1)

		if subscriber.is_subscribed(ticker_name):
			subscriber.unsubscribe(ticker_name)
			db.session.commit()

			return ok_request(params, 1)
		else:
			message = f'You are not subscribed to {ticker_name} ticker yet.'
			return no_content(params, message)