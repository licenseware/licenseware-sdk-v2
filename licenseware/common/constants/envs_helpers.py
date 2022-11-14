import os
import re

from pymongo import MongoClient


def mongo_connection_ok(mongo_uri: str):
    try:
        client = MongoClient(
            mongo_uri, serverSelectionTimeoutMS=2000, connectTimeoutMS=2000
        )
        client.list_databases()
        return True
    except:
        return False


def get_mongo_connection_string():

    uri = {
        "simple_uri": "mongodb://localhost:27017/db",
        "debug_uri": "mongodb://lware:lware-secret@localhost:27017",
        "stack_uri": "mongodb://lware:lware-secret@mongo:27017",
    }

    debug_data = None
    if os.path.exists("./deploy/.env.debug"):
        with open("./deploy/.env.debug", "r") as f:
            debug_data = f.read()
        m = re.search(r".*" + "MONGO_CONNECTION_STRING" + r"=(.+).*", debug_data)
        if m:
            uri["debug_uri"] = m.group(1)

    if debug_data is not None:

        SERVICE_NAME = None
        m = re.search(r".*" + "SERVICE_NAME" + r"=(.+).*", debug_data)
        if m:
            SERVICE_NAME = m.group(1)

            if os.path.exists("./deploy/.env." + SERVICE_NAME):

                with open("./deploy/.env." + SERVICE_NAME, "r") as f:
                    data = f.read()

                m = re.search(r".*" + "MONGO_CONNECTION_STRING" + r"=(.+).*", data)
                if m:
                    uri["stack_uri"] = m.group(1)

    for mongo_uri in uri:
        # print("Trying: ", uri[mongo_uri])
        if mongo_connection_ok(uri[mongo_uri]):
            print("Connection ok for: ", uri[mongo_uri])
            os.environ["MONGO_CONNECTION_STRING"] = uri[mongo_uri]
            return uri[mongo_uri]


def get_upload_path_on_desktop():

    default_upload_path = os.path.join(os.getcwd(), "uploaded_files")
    upload_path_file = os.path.join(os.getcwd(), "upload_path.txt")
    if os.path.exists(upload_path_file):
        with open(upload_path_file, "r") as f:
            upload_path = f.read()
        if upload_path == "":
            return default_upload_path
        else:
            return upload_path

    return default_upload_path


def get_env_var(var: str):
    try:
        return os.environ[var]
    except KeyError:
        raise Exception(f"Could not load environment variable: {var}")
