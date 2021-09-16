from dotenv import load_dotenv
load_dotenv()  

from flask import Flask
from app import App




app = Flask(__name__)

App.init_app(app)






if __name__ == "__main__":   
    
    App.register_app()
    
    app.run(port=4000, debug=True)