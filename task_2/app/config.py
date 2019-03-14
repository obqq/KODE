import os
import logging

class Config:
	COMPANY_NAME = 'Ticker Subscription Service'
	SERVER_NAME = '127.0.0.1:5000'

	# Interval of tickers update in seconds
	BACKGROUND_TASK_INTERVAL = 3600

	# alphavantage.co
	AV_API_KEY = os.environ.get('AV_API_KEY')

	MAIL_SERVER = ''
	MAIL_PORT = 465
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

	APP_MAIL_SUBJECT_PREFIX = f'[{COMPANY_NAME}]'
	APP_MAIL_SENDER = MAIL_USERNAME

	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	LOGGING_LEVEL = logging.DEBUG

	user = ''
	password = os.getenv('DB_PASSWORD')
	db_name = ''

	SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{db_name}'

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True


class TestingConfig(Config):
	TESTING = True


class ProductionConfig(Config):
	LOGGING_LEVEL = logging.INFO


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
