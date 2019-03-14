from threading import Thread
from flask import current_app, render_template, url_for
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
	with app.app_context():
		try:
			mail.send(msg)
		except Exception as e:
			app.logger.error(e)


def send_email(to, subject, template, **kwargs):
	app = current_app._get_current_object()
	company_name = app.config['COMPANY_NAME']

	msg = Message(app.config['APP_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
				  sender=app.config['APP_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', company_name=company_name, **kwargs)
	msg.html = render_template(template + '.html', company_name=company_name, **kwargs)
	thr = Thread(target=send_async_email, args=[app, msg])
	thr.start()
	return thr


def send_notification(email, message):
	unsubscribe_url = url_for('api.delete_subscription', email=email, _external=True)
	unsubscribe_ticker_url = url_for('api.delete_subscription',
									 email=email, _external=True)

	send_email(to=email, subject='Ticker Notification',
			   template='email/notification',
			   message=message, unsubscribe_url=unsubscribe_url,
			   unsubscribe_ticker_url=unsubscribe_ticker_url)


def send_on_new_subscription(email, ticker_name):
	unsubscribe_url = url_for('api.delete_subscription', email=email, _external=True)
	unsubscribe_ticker_url = url_for('api.delete_subscription', email=email,
									 ticker=ticker_name, _external=True)

	send_email(to=email, subject='Ticker Subscription',
			   template='email/new_subscription', ticker_name=ticker_name,
			   unsubscribe_url=unsubscribe_url,
			   unsubscribe_ticker_url=unsubscribe_ticker_url)
