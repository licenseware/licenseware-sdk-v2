"""

Notice we are using `marshmallow_to_restx_model` function to generate the swagger body required for the request. 
Notice also the separation of creating the resource and the given namespace. 

"""

from flask import request
from flask_restx import Namespace, Resource
from marshmallow import Schema, fields

from licenseware.common import marshmallow_to_restx_model
from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.uploader_encryptor import UploaderEncryptor


class ExpectSchema(Schema):
    decrypt_password = fields.String()
    encrypted_values = fields.List(fields.String)


class DecryptedValuesSchema(Schema):
    encrypted_value = fields.String()
    decrypted_value = fields.String()


class ResponseSchema(Schema):
    decrypted_values = fields.List(fields.Nested(DecryptedValuesSchema))


def get_decrypt_namespace(ns: Namespace):

    expect_model = marshmallow_to_restx_model(ns, ExpectSchema)
    response_model = marshmallow_to_restx_model(ns, ResponseSchema)

    @ns.route("")
    class Decrypt(Resource):
        @failsafe(fail_code=500)
        @ns.doc(
            description="Decrypt provided list of encrypted values using the password provided"
        )
        @ns.expect(expect_model, validate=True)
        @ns.response(200, "Decrypted values", response_model)
        @authorization_check
        def post(self):

            data = request.json
            ue = UploaderEncryptor()
            ue.set_password(data["decrypt_password"])

            decrypted_values = [
                {
                    "encrypted_value": encrypted_value,
                    "decrypted_value": ue.decrypt(encrypted_value),
                }
                for encrypted_value in set(data["encrypted_values"])
            ]

            return decrypted_values

    return ns
