from licenseware.namespace_generator.schema_namespace import SchemaNamespace



def namespace(**dkwargs):
	""" 
		This is a class decorator which receives SchemaNamespace keyword arguments

		# Here DeviceService handles specific data manipulation on post, delete requests

		@namespace(schema=DeviceSchema, collection='IFMPData')
		class DeviceNamespace:

			def post(self):
				tenant_id = request.headers.get("TenantId")
				return DeviceService.replace_one(json_data=request.json, tenant_id=tenant_id)

			def delete(self, _id=None):
				tenant_id = request.headers.get("TenantId")
				_id = request.args.get("_id")
				return DeviceService.delete_one(_id=_id, tenant_id=tenant_id)
		
	"""

	def wrapper(cls):
		newcls = type(cls.__name__, (cls, SchemaNamespace,), {**dkwargs})
		return lambda: newcls._initialize()
	return wrapper
