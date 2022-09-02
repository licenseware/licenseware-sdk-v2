def extract_query_string(req_data):

    parameters = req_data.get("parameters") if isinstance(req_data, dict) else req_data
    if not parameters:
        return

    query_string = {}
    for data in parameters:

        if not data.get("in"):
            continue
        if data["in"] != "query":
            continue

        for k, v in data.items():
            if k == "name":
                query_string[data["name"]] = data["type"]

    return query_string if query_string else None


def extract_headers(req_data):
    # TODO extract security headers

    headers = {}
    if req_data.get("parameters"):
        for data in req_data["parameters"]:
            if not data.get("in"):
                continue
            if data["in"] != "header":
                continue
            for k, v in data.items():
                if k == "name":
                    headers[data["name"]] = data["type"]

    return headers if headers else None


def create_init_file(init_file_path, test_email, test_password):
    util_funcs = """

def increase_quota(uploader_id: str):
    with collection(envs.MONGO_COLLECTION_UTILIZATION_NAME) as col:
        res = col.find_one(filter={"uploader_id": uploader_id})
        if res is None:
            return
        if res["monthly_quota"] <= 1:
            col.update_one(
                filter={"uploader_id": uploader_id},
                update={"$inc": {"monthly_quota": 9999}},
            )


def clear_quota():
    with collection(envs.MONGO_COLLECTION_UTILIZATION_NAME) as col:
        col.delete_many({})


def clear_db():

    cols = [
        envs.MONGO_COLLECTION_UTILIZATION_NAME,
        envs.MONGO_COLLECTION_ANALYSIS_NAME,
        envs.MONGO_COLLECTION_HISTORY_NAME,
        envs.MONGO_COLLECTION_TOKEN_NAME,
        envs.MONGO_COLLECTION_DATA_NAME,
    ]
    
    for name in cols:
        with collection(name) as col:
            col.delete_many({})


"""

    with open(init_file_path, "w") as f:
        f.write(
            f"""
import os
from licenseware.common.constants import envs
from licenseware.mongodata import collection

test_email = "{test_email}"
test_password = "{test_password}" 

if os.path.exists("coverage.svg"):
    os.remove("coverage.svg")
"""
            + util_funcs
        )


def create_test_file(test_path, contents):
    with open(test_path, "w") as f:
        f.write(contents)


def order_by_request(request_data):

    req_order = ["post", "get", "put", "delete"]

    desiredidx = []
    for req in req_order:
        for cidx, data in enumerate(request_data):
            if req == data["method"]:
                desiredidx.append(cidx)

    orderedby_request = [request_data[cidx] for cidx in desiredidx]

    return orderedby_request
