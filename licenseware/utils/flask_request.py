import io
import os

from werkzeug.datastructures import FileStorage


def get_request_files(*file_paths):
    """
    This takes a file path and creates a FileStorage object needed by flask
    Make sure to put the result from this function in a dictionary
    Ex: {"files[]": get_request_files(myFilePath1, myFilePath2, etc)}
    """

    file_storage_files = []
    for fpath in file_paths:
        with open(fpath, "rb") as f:
            file_binary = io.BytesIO(f.read())

        fs_file = FileStorage(
            stream=file_binary,
            filename=os.path.basename(fpath),
            content_type="application/*",
        )

        file_storage_files.append(fs_file)

    return file_storage_files


def get_flask_request(
    headers: dict = None,
    args: dict = None,
    json: dict = None,
    files: list = []
    # decorators: List[Callable] = [] #TODO
):
    """
    Build an equivalent to flask request object which can be used in tests.
    """

    class MockFlaskRequest:

        headers_data = {}
        args_data = {}
        files_data = {}
        json = None

        class headers:
            @staticmethod
            def get(val):
                arg = MockFlaskRequest.headers_data.get(val)
                if arg is None:
                    return None
                return str(arg)

        class files:
            @staticmethod
            def getlist(val):
                arg = MockFlaskRequest.files_data.get(val)
                if arg is None:
                    return None
                return str(arg)

        class args:
            @staticmethod
            def get(val):
                arg = MockFlaskRequest.args_data.get(val)
                if arg is None:
                    return None
                return str(arg)

    MockFlaskRequest.json = json
    MockFlaskRequest.headers_data = headers if headers is not None else {}
    MockFlaskRequest.args_data = args if args is not None else {}
    MockFlaskRequest.files_data = {"files[]": get_request_files(files)} if files else {}

    return MockFlaskRequest
