#!/usr/bin/env python
import web
import MySQLdb
import json
import hashlib
import os

urls = (
	'/login', 'login',
	'/logout', 'logout',
	'/check-token', 'checkToken',
)

app = web.application(urls, globals())

db = web.database(dbn = 'mysql', db = 'python-restful-api', user = 'DB-USER', pw = 'DB-PASS')

class login:
	def POST(self):
		response = {'ok': 1, 'errorCode': '200', 'errorMessage': None, 'data': {}}
		
		data = json.loads(web.data())

		# Input data validation
		if not 'username' in data or not 'password' in data:
			response['ok'] = 0
			response['errorCode'] = 400
			response['errorMessage'] = 'Invalid input data.'

			return json.dumps(response)

		username = data['username']
		password = data['password']

		result = db.query('SELECT * FROM users WHERE username = \'{}\' AND password = \'{}\''.format(username, password))
		user = result.first()

		# Check if the record exists at the database
		if user == None:
			response['ok'] = 0
			response['errorCode'] = 403
			response['errorMessage'] = 'Authentication failed.'

		else:
			token = hashlib.sha1(os.urandom(32)).hexdigest()
			query = db.query('REPLACE INTO tokens (user_id, token) VALUES ({}, \'{}\')'.format(user.id, token))
			response['data'].update({'token': token})

		return json.dumps(response)

class logout:
	def POST(self):
		response = {'ok': 1, 'errorCode': '200', 'errorMessage': None, 'data': {}}
		
		data = json.loads(web.data())

		# Input data validation
		if not 'token' in data:
			response['ok'] = 0
			response['errorCode'] = 400
			response['errorMessage'] = 'Invalid input data.'

			return json.dumps(response)

		token = data['token']

		db.delete('tokens', where = 'token = \'{}\''.format(token))

		return json.dumps(response)

class checkToken:
	def POST(self):
		response = {'ok': 1, 'errorCode': '200', 'errorMessage': None, 'data': {}}
		
		data = json.loads(web.data())

		# Input data validation
		if not 'token' in data:
			response['ok'] = 0
			response['errorCode'] = 400
			response['errorMessage'] = 'Invalid input data.'

			return json.dumps(response)

		token = data['token']

		result = db.query('SELECT * FROM tokens WHERE token = \'{}\''.format(token))

		# Check if the record exists at the database
		if result.first() == None:
			response['ok'] = 0
			response['errorCode'] = 401
			response['errorMessage'] = 'Unauthorized request.'

		return json.dumps(response)

if __name__ == '__main__':
	app.run()