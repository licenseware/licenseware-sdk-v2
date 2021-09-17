from flask import Flask


app = Flask(__name__)


_id = '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<string:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all_routes(path):
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'Tenantid': _id,
        'user_id': _id
    }, 200
       
       

if __name__ == '__main__':
    app.run(debug=True)