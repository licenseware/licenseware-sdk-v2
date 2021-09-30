from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from app import App




app = Flask(__name__)

App.init_app(app)
App.register_app()






if __name__ == "__main__":   
    app.run(port=5000, debug=True)