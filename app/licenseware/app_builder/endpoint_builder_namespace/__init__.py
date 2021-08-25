from flask_restx import Namespace



endpoint_builder_namespace = Namespace(
    name="Endpoint Builder",
    description="Routes created with EndpointBuilder",
    path='/custom_endpoint'
)
