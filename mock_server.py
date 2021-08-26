from flask import Flask


app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<string:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all_routes(path):
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200
       
       

if __name__ == '__main__':
    app.run(debug=True)