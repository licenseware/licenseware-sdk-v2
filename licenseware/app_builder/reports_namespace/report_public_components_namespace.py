from typing import List

from flask import request
from flask_restx import Namespace, Resource, fields

from licenseware.decorators import failsafe
from licenseware.decorators.auth_decorators import public_token_check
from licenseware.report_builder import ReportBuilder
from licenseware.report_components import BaseReportComponent


def create_individual_report_component_resource(component: BaseReportComponent):
    class ComponentRes(Resource):
        @failsafe(fail_code=500)
        @public_token_check
        def post(self):
            return component.get_data(request)

        @failsafe(fail_code=500)
        @public_token_check
        def get(self):
            return component.get_data(request)

    return ComponentRes


def get_public_report_components_namespace(ns: Namespace, reports: List[ReportBuilder]):

    restx_model = ns.model(
        "ComponentFilter",
        dict(
            column=fields.String,
            filter_type=fields.String,
            filter_value=fields.List(fields.String),
        ),
    )

    for report in reports:
        for comp in report.components:
            ComponentRes = create_individual_report_component_resource(comp)

            params = {}
            params[comp.component_id + "_limit"] = {
                "description": "Limit the number of results"
            }
            params[comp.component_id + "_skip"] = {
                "description": "Skip the first n results"
            }

            docs = {
                "get": {
                    "description": "Get public component data",
                    "params": {
                        **params,
                        "public_token": {
                            "description": "The token which will be used to return data"
                        },
                    },
                    "responses": {
                        200: "Success",
                        403: "Public token missing or invalid",
                        500: "Something went wrong while handling the request",
                    },
                },
                "post": {
                    "description": "Get public component data with an optional filter payload",
                    "params": {
                        **params,
                        "public_token": {
                            "description": "The token which will be used to return data"
                        },
                    },
                    "validate": None,
                    "expect": [restx_model],
                    "responses": {
                        200: "Success",
                        403: "Public token missing or invalid",
                        500: "Something went wrong while handling the request",
                    },
                },
            }

            ComponentRes.__apidoc__ = docs

            IRCResource = type(
                comp.component_id.replace("_", "").capitalize()
                + "public_individual_component",
                (ComponentRes,),
                {},
            )

            ns.add_resource(
                IRCResource, report.report_path + comp.public_component_path
            )

    return ns
