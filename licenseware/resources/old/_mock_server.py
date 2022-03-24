from flask import Flask


app = Flask(__name__)


tenant_id = '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'
user_id = '6aae241f-cee2-455f-9ec7-5a63b4a50316'


tenants = [
    {
        'id': tenant,
        'company_name': "tenant.company_name",
        'is_default': True,
        'registered_on': "tenant.registered_on"
    } for tenant in [tenant_id]
]


@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route("/<string:path>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def catch_all_routes(path):
    return {
        'status': 'success', 
        'Authorization': 'long_auth_token',
        'Tenantid': tenant_id,
        'user_id': user_id,
        'data': tenants,
        "id": user_id,
        "email": 'user.email',
        "first_name": 'user.first_name',
        "last_name": 'user.last_name',
        "company_name": 'user.company_name',
        "job_title": 'user.job_title',
        "plan_type": 'UNLIMITED',
        "email_verified": True,
        "profile_pic": 'user.profile_pic'
    }, 200
       
       

if __name__ == '__main__':
    app.run(debug=True)