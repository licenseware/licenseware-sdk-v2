from flask import Flask


app = Flask(__name__)



@app.route('/')
def index():
    return 'Auth service mock server'
  
       
@app.route('/ifmp/app', methods=['GET'])
def ifmp_app():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200


@app.route('/ifmp/app/init', methods=['GET'])
def app_init():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200
      

@app.route('/ifmp/refresh_registration', methods=['GET'])
def refresh_registration():
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'TenantId': 'uuid4_tenant_id',
    }, 200
      

      
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


@app.route('/auth/machine_authorization', methods=['GET'])
def machine_authorization():
    return {
            'status': 'success', 
            'Authorization': 'long_auth_token',
            'TenantId': 'uuid4_tenant_id',
        }, 200


@app.route('/auth/verify', methods=['GET'])
def user_authorization():
    return {
            'status': 'success', 
            'Authorization': 'long_auth_token',
            'TenantId': 'uuid4_tenant_id',
        }, 200


@app.route('/registry-service/apps', methods=['POST'])
def register_app():
    return {'status': 'success'}, 200

@app.route('/registry-service/uploaders', methods=['POST'])
def register_uploader():
    return {'status': 'success'}, 200

@app.route('/registry-service/reports', methods=['POST'])
def register_report():
    return {'status': 'success'}, 200


@app.route('/registry-service/reports/components', methods=['POST'])
def register_report_component():
    return {'status': 'success'}, 200




if __name__ == '__main__':
    app.run(debug=True)