from flask import request
from .mongo_crud import MongoCrud


class MongoRequest(MongoCrud):
	"""
		This class provides get, post, put, delete http methods.

		Needs a TenantId in the request header.	
		Decorator authorization_check makes sure that TenantId and auth_token are provided

		Query params are taken from request.args, '_id' parameter is just for swagger documentation.

	"""

	def get(self, _id=None):
		if 'GET' in self.methods: 
			return self.fetch_data(request) 
		return "METHOD NOT ALLOWED", 405

	def post(self):
		if 'POST' in self.methods:
			return self.insert_data(request) 
		return "METHOD NOT ALLOWED", 405
		
	def put(self):
		if 'PUT' in self.methods:
			return self.update_data(request) 
		return "METHOD NOT ALLOWED", 405
		
	def delete(self, _id=None):
		if 'DELETE' in self.methods:
			return self.delete_data(request) 
		return "METHOD NOT ALLOWED", 405

