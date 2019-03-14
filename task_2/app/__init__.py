import atexit
import logging
from logging.handlers import RotatingFileHandler

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from .config import config

mail = Mail()
db = SQLAlchemy()


def create_scheduler(flask_app):
	from app.tasks import update_tickers
	'''
	Setting up background task (updating tickers)
	I thought celery would be overkill 
	'''

	scheduler = BackgroundScheduler()
	scheduler.add_job(func=update_tickers, trigger="interval",
					  seconds=flask_app.config['BACKGROUND_TASK_INTERVAL'], args=[flask_app])

	atexit.register(lambda: scheduler.shutdown())
	return scheduler


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config['default'].init_app(app)

	file_handler = RotatingFileHandler('app.log', maxBytes=(1048576 * 5), backupCount=10)
	file_handler.setLevel(app.config['LOGGING_LEVEL'])
	file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
	app.logger.addHandler(file_handler)

	mail.init_app(app)

	with app.app_context():
		db.init_app(app)
		db.create_all()

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/')

	scheduler = create_scheduler(app)
	scheduler.start()

	app.logger.info('Started background task')

	return app
