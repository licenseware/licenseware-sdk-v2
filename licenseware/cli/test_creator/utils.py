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
    with open(init_file_path, "w") as f:
        f.write(f"""
import warnings

warnings.filterwarnings("ignore")

test_email = "{test_email}"
test_password = "{test_password}" 

""")


def create_test_file(test_path, contents):
    with open(test_path, "w") as f:
        f.write(contents)


def order_by_request(request_data):

    req_order = ["get", "post", "put", "delete"]

    desiredidx = []
    for req in req_order:
        for cidx, data in enumerate(request_data):
            if req == data["method"]:
                desiredidx.append(cidx)

    orderedby_request = [request_data[cidx] for cidx in desiredidx]

    return orderedby_request
