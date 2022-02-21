from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.utils.logger import log
from licenseware.decorators.auth_decorators import authorization_check
from licenseware.report_components.base_report_component import BaseReportComponent
from licenseware.decorators import failsafe

from licenseware.download import download_as


def create_individual_report_component_resource(component: BaseReportComponent):
    class ComponentRes(Resource):

        @failsafe(fail_code=500)
        @authorization_check
        def post(self):
            return component.get_data(request)

        @failsafe(fail_code=500)
        @authorization_check
        def get(self):
            file_type = request.args.get('download_as')
            tenant_id = request.headers.get('Tenantid')
            data = component.get_data(request)

            if file_type is None:
                return data

            return download_as(
                file_type,
                data,
                tenant_id,
                filename=component.component_id
            )

    return ComponentRes


def get_report_individual_components_namespace(ns: Namespace, report_components: list):
    restx_model = ns.model('ComponentFilter', dict(
        column=fields.String,
        filter_type=fields.String,
        filter_value=fields.List(fields.String)
    )
                           )

    for comp in report_components:
        ComponentRes = create_individual_report_component_resource(comp)

        docs = {
            'get': {
                'description': 'Get component data',
                'params': {'download_as':
                    {
                        'description': 'Download table component as file type: csv, xlsx, json'
                    }
                },
                'responses': {
                    200: 'Success',
                    403: 'Missing `Tenantid` or `Authorization` information',
                    500: 'Something went wrong while handling the request'
                }
            },
            'post': {
                'description': 'Get component data with an optional filter payload',
                'validate': None,
                'expect': [restx_model],
                'responses': {
                    200: 'Success',
                    403: 'Missing `Tenantid` or `Authorization` information',
                    500: 'Something went wrong while handling the request'
                }
            }
        }

        ComponentRes.__apidoc__ = docs

        IRCResource = type(
            comp.component_id.replace("_", "").capitalize() + 'individual_component',
            (ComponentRes,),
            {}
        )

        ns.add_resource(IRCResource, comp.component_path)

    return ns
