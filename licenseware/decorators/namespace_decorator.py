from licenseware.namespace_generator.schema_namespace import SchemaNamespace



def namespace(**dkwargs):
	""" 
		This is a class decorator which receives SchemaNamespace keyword arguments

		# Here DeviceService handles specific data manipulation on post, delete requests

		@namespace(schema=DeviceSchema, collection='IFMPData')
		class DeviceNamespace:

			#TODO docs
    
    
		App.add_namespace(DeviceNamespace())
		
	"""

	def wrapper(cls):
		newcls = type(cls.__name__, (cls, SchemaNamespace,), {**dkwargs})
		return lambda: newcls._initialize()
	return wrapper
