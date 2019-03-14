from flask import request, jsonify
from flask.app import BadRequest

from functools import wraps
from jsonschema import validate

from jsonschema.exceptions import ValidationError
from .json_schemas import schemas
from .errors import bad_request, validation_error


def validate_json(f):
	@wraps(f)
	def wrapper(*args, **kw):
		try:
			request.json
		except BadRequest as e:
			message = 'Failed to decode JSON object'
			return bad_request(message=message, params={})
		return f(*args, **kw)

	return wrapper


def validate_schema(schema_name):
	def decorator(f):

		@wraps(f)
		def wrapper(*args, **kw):
			try:
				validate(request.json, schemas.get(schema_name))
			except ValidationError as e:
				return validation_error(request.json, e.message)
			return f(*args, **kw)

		return wrapper

	return decorator
