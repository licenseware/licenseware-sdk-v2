from typing import List





class UploaderEncrytor:

    """

    This class will use AES encryption algorithm to encrypt files given.

    Params:

    filenames = ["(.*_.*_)options.csv"], # encrypt text found with regex from filenames   
    filepaths = ["Collection-(.*)"], # this will encrypt things like `/Collection-devicename/path/dir`
    filecontent = ["ODBName(.*)"], # encrypt text found with regex from file content (csv, txt, xml) replace all
    columns = ["OS", "IP"] # encrypt the entire column data where the specified columns are found (csv, excel with multiple sheets)

    """

    def __init__(
        self,
        filenames: List[str] = None,
        filepaths: List[str] = None,
        filecontent: List[str] = None,
        columns: List[str] = None
    ):

        self.filenames = filenames or []
        self.filepaths = filepaths or []
        self.filecontent = filecontent or []
        self.columns =columns or []



    def encrypt_file(filepath: str):
        pass

