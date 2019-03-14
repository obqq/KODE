from . import db


class Subscriber(db.Model):
	__tablename__ = 'subscribers'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(254), unique=True, index=True)
	subscriptions = db.relationship('Subscription', backref='subscriber', lazy='dynamic')

	def subscribe(self, ticker_name, max_price, min_price):
		f = Subscription(subscriber_id=self.id,
						 ticker_name=ticker_name,
						 max_price=max_price,
						 min_price=min_price)
		db.session.add(f)

	def unsubscribe(self, ticker_name):
		f = self.subscriptions.filter_by(ticker_name=ticker_name).first()
		if f:
			db.session.delete(f)

	def is_subscribed(self, ticker_name):
		return self.subscriptions.filter_by(ticker_name=ticker_name).first() is not None

	def __repr__(self):
		return f'{self.id}:{self.email}:{self.subscriptions}'


class Subscription(db.Model):
	__tablename__ = 'subscriptions'
	id = db.Column(db.Integer, primary_key=True)
	subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'))
	ticker_name = db.Column(db.String(64))
	max_price = db.Column(db.Integer)
	min_price = db.Column(db.Integer)
