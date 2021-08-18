from flask_restx import Namespace





app_namespace = Namespace(
    name='App',
    description='App related base routes',
    prefix='/app'
)