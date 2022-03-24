import os
from trend_app_protect import wrap_wsgi_app
from flask import Flask
from app import App

app = Flask(__name__)

App.init_app(app)
App.register_app()

# Trend Micro `Application Security`
if os.getenv('ENVIRONMENT') in {'prod', 'production'}:
    app = wrap_wsgi_app(app)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
