import os
from app import create_app, db
from app.models import Subscriber, Subscription

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
	load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, Subscriber=Subscriber, Subscription=Subscription)


@app.cli.command()
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
	app.run(host='127.0.0.0', port=5000, debug=True)
