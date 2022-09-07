import importlib.resources as pkg_resources
import json
import os
import re

import requests
from jinja2 import Template

from licenseware.cli.test_creator import templates, utils

allowed_requests = ["GET", "PUT", "POST", "DELETE", "OPTIONS"]


class TestCreator:
    def __init__(
        self,
        swagger: str,
        email: str,
        password: str = None,
        auth_headers: dict = None,
        test_path: str = "./tests",
        ignore_files: list = None,
        overwrite_files: bool = False,
    ):

        self.swagger = swagger
        self.swagger_url = swagger if swagger.startswith("http:") else None
        self.swagger_path = swagger if not swagger.startswith("http:") else None
        self.test_path = test_path
        self.ignore_files = ignore_files
        self.overwrite_files = overwrite_files
        self.email = email
        self.password = password
        self.auth_headers = auth_headers
        self.swagger_docs = self.get_swagger_docs()

    def get_swagger_docs_from_url(self):
        # 'http://localhost/dsa-service/swagger.json'
        # 'http://localhost:5000/dsa-service/swagger.json'
        try:
            return requests.get(self.swagger_url, timeout=5).json()
        except:
            try:
                return requests.get(
                    self.swagger_url.replace("localhost", "localhost:5000"), timeout=5
                ).json()
            except:
                try:
                    return requests.get(
                        self.swagger_url.replace("-service", ""), timeout=5
                    ).json()
                except:
                    raise Exception(f"URL: {self.swagger_url} not responding")

    def get_swagger_docs_from_path(self):
        with open(self.swagger_path, "r") as j:
            return json.load(j)

    def get_swagger_docs(self):
        if self.swagger_url:
            return self.get_swagger_docs_from_url()
        elif self.swagger_path:
            return self.get_swagger_docs_from_path()

    def get_file_url(self):
        paths = self.swagger_docs["paths"].keys()
        file_url = {}
        for path in paths:
            route = path
            path = re.sub(r"[^\w\s]", "_", path[1:])
            path = re.sub(r"_{2,100}", "_", path)
            if path.endswith("_"):
                path = path[:-1]
            test_filename = "test_" + path + ".py"
            file_url[test_filename] = route
        return file_url

    def parse_schema(self, tag):

        # print("parse_schema", tag)

        payload = {}

        match = re.search(r"#/definitions/(.*?)Schema", tag)
        if match:
            tag_no_schema = match.group(1)
        else:
            tag_no_schema = None

        tag_raw = tag.replace("#/definitions/", "")

        if "definitions" not in self.swagger_docs:
            return payload

        schema1 = self.swagger_docs["definitions"].get(tag_no_schema)
        schema2 = self.swagger_docs["definitions"].get(tag_raw)

        tag = tag_no_schema if schema1 else tag_raw

        schema = schema1 or schema2
        if not schema:
            return payload

        required_fields = self.swagger_docs["definitions"][tag].get("required")
        required_fields = required_fields if required_fields else []

        for field, val in schema["properties"].items():

            # Nested list fields
            if val.get("type") == "array":
                if val.get("items"):
                    schema_path = val["items"].get("$ref")
                    if not schema_path:
                        payload[field] = [val["items"].get("type")]
                    else:
                        tag = val["items"]["$ref"]
                        payload[field] = self.parse_schema(tag)
                else:
                    payload[field] = []

            # Simple nest
            elif val.get("$ref"):
                tag = val["$ref"]
                payload[field] = self.parse_schema(tag)

            # Simple fields
            elif val.get("type"):
                field_type = (
                    val["type"] + "_required"
                    if field in required_fields
                    else val["type"]
                )
                payload[field] = field_type

        return payload

    def payload_from_parameters(self, req_data):

        payload = {}
        for data in req_data["parameters"]:
            if not data.get("schema"):
                continue
            tag = data["schema"].get("$ref")
            if not tag:
                continue
            parsed_payload = self.parse_schema(tag)
            payload.update(parsed_payload)

        # print("payload_from_parameters", payload)

        return payload

    def payload_from_tags(self, req_data):
        payload = {}

        if "definitions" not in self.swagger_docs:
            return payload

        for tag in req_data["tags"]:
            schema = self.swagger_docs["definitions"].get(tag)
            if not schema:
                tag = tag + "Schema"
                schema = self.swagger_docs["definitions"].get(tag)

            if not schema:
                continue

            required_fields = self.swagger_docs["definitions"][tag]["required"]

            for field, val in schema["properties"].items():
                val = (
                    val["type"] + "_required"
                    if field in required_fields
                    else val["type"]
                )
                payload[field] = val

        return payload

    def extract_payload(self, req_data):
        if req_data.get("parameters"):
            payload = self.payload_from_parameters(req_data)
            return payload if payload else None

        if req_data.get("tags"):
            payload = self.payload_from_tags(req_data)
            return payload if payload else None

    def get_request_data(self, route: str):

        request_info = self.swagger_docs["paths"][route]

        requests_data = []
        query_string = None
        for req_type, req_data in request_info.items():

            data = {}
            if not query_string:
                query_string = utils.extract_query_string(req_data)

            if req_type.upper() not in allowed_requests:
                continue
            data["query_string"] = query_string
            data["method"] = req_type
            data["headers"] = utils.extract_headers(req_data)
            data["payload"] = (
                self.extract_payload(req_data) if req_type != "get" else None
            )
            data["doc"] = req_data.get("description") or req_data.get("operationId")
            data["route"] = route

            # files = {}
            # data['files'] = files

            requests_data.append(data)

        return utils.order_by_request(requests_data)

    def generate_test_file_contents(self, file_url: dict):
        file_contents_dict = {}
        for file, route in file_url.items():
            func_name = file.replace(".py", "")
            request_data = self.get_request_data(route)

            # fpath = os.path.join(self.test_path, file)
            raw_contents = pkg_resources.read_text(templates, "test_template.jinja")
            tmp = Template(raw_contents, trim_blocks=True, lstrip_blocks=True)
            file_contents = tmp.render(
                test_file_name=file,
                test_function_name=func_name,
                email=self.email,
                request_data=request_data,
            )

            file_contents_dict[file] = file_contents

        return file_contents_dict

    def write_default_test_files(self, file_contents_dict):

        if not os.path.exists(self.test_path):
            os.makedirs(self.test_path)

        init_file_path = os.path.join(self.test_path, "__init__.py")
        init_exists = os.path.isfile(init_file_path)

        if self.overwrite_files:
            utils.create_init_file(init_file_path, self.email, self.password)
        if not init_exists:
            utils.create_init_file(init_file_path, self.email, self.password)

        for filename, contents in file_contents_dict.items():
            filename = "_" + filename
            if self.ignore_files is not None:
                if filename in self.ignore_files:
                    continue
            test_path = os.path.join(self.test_path, filename)
            test_exists = os.path.isfile(
                os.path.join(self.test_path, filename[1:])
            ) or os.path.isfile(test_path)

            if self.overwrite_files:
                utils.create_test_file(test_path, contents)
            if not test_exists:
                utils.create_test_file(test_path, contents)

    def generate_tests(self):
        file_url = self.get_file_url()
        file_contents_dict = self.generate_test_file_contents(file_url)
        self.write_default_test_files(file_contents_dict)
