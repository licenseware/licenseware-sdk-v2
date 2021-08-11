from flask import Flask


app = Flask(__name__)


# self.assertEqual(envs.AUTH_USERS_URL, 'http://localhost:5000/auth/users')
# self.assertEqual(envs.AUTH_MACHINES_URL, 'http://localhost:5000/auth/machines')

        
@app.route('/')
def index():
    return 'Auth service mock server'
        
        
@app.route('/auth/users/login', methods=['POST'])
def login_user():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200


@app.route('/auth/machines/login', methods=['POST'])
def login_machines():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200
    
    
@app.route('/auth/users/create', methods=['POST'])
def create_user():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200


@app.route('/auth/machines/create', methods=['POST'])
def create_machines():
    return {
            'status': 'success', 
            'Authorization': 'long_auth_token',
            'TenantId': 'uuid4_tenant_id',
        }, 200



@app.route('/registry-service/apps', methods=['POST'])
def registry_service():
    return {'status': 'success'}, 200




if __name__ == '__main__':
    app.run(debug=True)