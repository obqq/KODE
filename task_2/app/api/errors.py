from flask import request, render_template, jsonify
from app.exceptions import ValidationError
from . import api


@api.errorhandler(405)
def method_not_allowed(e):
	message = 'Please, use POST request method'
	response = jsonify({'error': {'code': 405,
								  'description': message},
						'data': None})
	response.status_code = 405
	return response


@api.errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		message = 'Endpoint not found'
		response = jsonify({'error': {'code': 400,
									  'description': message},
							'data': None})
		response.status_code = 404
		return response
	return render_template('404.html'), 404


@api.errorhandler(400)
def bad_request(params, message='Bad Request'):
	response = jsonify(
		{'error': {'code': 400,
				   'description': message},
		 'data': params})
	response.status_code = 400
	return response\


def no_content(params, message='No content'):
	response = jsonify(
		{'error': {'code': 204,
				   'description': message},
		 'data': params})
	response.status_code = 204
	return response


@api.errorhandler(ValidationError)
def validation_error(params, message):
	return bad_request(params, message)
