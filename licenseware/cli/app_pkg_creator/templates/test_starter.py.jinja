import pytest
from flask.testing import Client
# Use mongodata for some seed data if needed (make sure to clean db after test)
from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.mongodata import collection
from licenseware.test_helpers.auth import AuthHelper
from licenseware.test_helpers.flask_request import get_flask_request, get_request_files
from licenseware.utils.logger import log
from main import app


@pytest.fixture
def c():
    with app.test_client() as client:
        yield client


def increase_quota():
    # Pretty common is to increase quota to make more requests
    with collection(envs.MONGO_COLLECTION_UTILIZATION_NAME) as col:
        res = col.find_one(filter={"uploader_id": "catalogs_quota"})
        if res is None:
            return
        if res["monthly_quota"] <= 1:
            col.update_one(
                filter={"uploader_id": "catalogs_quota"},
                update={"$inc": {"monthly_quota": 9999}},
            )


# tox tests/test_*
# tox tests/test_starter.py

# tox tests/test_starter.py::test_something_specific
def test_something_specific(c: Client):
    # Will create an account or login and return the auth headers needed for making requests
    auth_headers = AuthHelper("alin+test@licenseware.io").get_auth_headers()

    response = c.get(f"{envs.APP_PATH}/activate_app", headers=auth_headers)
    assert response.status_code, 200

    increase_quota()

    # define a post/put etc payload
    payload = [
        {"some": "data"}
    ]

    response = c.post(f"{envs.APP_PATH}/some-endpoint", json=payload, headers=auth_headers)
    log.warning(response.data)  # view what's returned for debugging

    # make some assertions
    assert response.status_code, 201

    # a get request with some query parameters
    # (ex: https://awesomewebsite.com/another-endpoint?search_value=test)
    response = c.get(
        f"{envs.APP_PATH}/another-endpoint",
        query_string={"search_value": "test"},
        headers=auth_headers,
    )

    assert response.status_code, 200

    # Upload some files
    response = c.post(
        f"{envs.APP_PATH}/uploads/uploader_id/files",
        data={"files[]": get_request_files(
            "./test_files/rl/file1.csv",
            "./test_files/rl/file2.csv",
            "./test_files/rl/file3.csv",
        )
        },
        headers=auth_headers
    )

    assert response.status_code, 200


# tox tests/test_starter.py::test_something_else
def test_something_else(c: Client):
    # Imported here just for demo
    from app.services.module import some_func

    auth_headers = AuthHelper("alin+test@licenseware.io").get_auth_headers()

    mimic_flask_request = get_flask_request(
        headers=auth_headers,
        args={"search_value": "test", "limit": 20, "skip": 40},
        json={"some": "payload"},
        files=["./test_files/somefile.xlsx"]  # will create a FileStorage object from paths given
    )

    # The flask mock request object created up is useful if you don't want to use flask TestClient
    # It's also useful for unit test the functions
    results = some_func(request=mimic_flask_request)

    assert results == "all good"
