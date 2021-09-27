from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from flask_cors import CORS
from app import App




app = Flask(__name__)

CORS(app)

App.init_app(app)






if __name__ == "__main__":   
    
    App.register_app()
    
    app.run(port=5000, debug=True)