"""

Validator for streams of files and files.


```py

from licenseware.common.validators.file_validators import GeneralValidator, validate_filename

v = GeneralValidator(
    input_object,           - required: file path, string or stream
    required_input_type = None,    - required: 'excel', 'csv', 'txt', 'string', 'stream'
    required_sheets   = [], - sheets names list that needs to be found in 'excel'
    required_columns  = [], - columns names list that needs to be found in 'excel', 'csv'
    text_contains_all = [], - text list that needs to be found in 'txt', 'string', 'stream'
    text_contains_any = [], - text list that needs to be found in 'txt', 'string', 'stream'
    min_rows_number   = 0,  - minimum rows needed for 'excel', 'csv'
    header_starts_at  = 0   - row number where the header with columns starts (count starts from 0)
    buffer = 9000           - bytes buffer to read from stream FileStorage object
)


valid_input = True

try:
    v.validate() # valid
except:
    valid_input = False # not valid



```

You can also import individually the function bellow:


"""


import itertools
import os
import re
from io import BytesIO

import pandas as pd

from licenseware.utils.logger import log


def validate_text_contains_all(text, text_contains_all, regex_escape=True):
    """
    Raise exception if contents of the text file don't contain all items in text_contains_all list
    """

    if not text_contains_all:
        return

    matches_count = 0
    for txt_to_find in text_contains_all:
        pattern = re.compile(
            re.escape(txt_to_find) if regex_escape else txt_to_find, flags=re.IGNORECASE
        )
        match = re.search(pattern, text)
        if match:
            matches_count += 1

    if matches_count < len(text_contains_all):
        raise ValueError(
            f'File must contain the all following keywords: {", ".join(text_contains_all)}'
        )


def validate_text_contains_any(text, text_contains_any, regex_escape=True):
    """
    Raise exception if contents of the text file don't contain at least one item in text_contains_any list
    """

    if not text_contains_any:
        return

    for txt_to_find in text_contains_any:
        pattern = re.compile(
            re.escape(txt_to_find) if regex_escape else txt_to_find, flags=re.IGNORECASE
        )
        match = re.search(pattern, text)
        if match:
            return

    raise ValueError(
        f'File must contain at least one of the following keywords: {", ".join(text_contains_any)}'
    )


def _columns_validator(file_columns, required_columns, raise_error=True):
    if isinstance(file_columns, list):
        common_cols = list(set.intersection(set(required_columns), set(file_columns)))
        if sorted(required_columns) != sorted(common_cols):
            missing_cols = set.difference(set(required_columns), set(file_columns))
            if raise_error:
                raise ValueError(
                    f"Table does not contain required columns: {missing_cols}"
                )
            return False
        return True
    else:
        if not all(col in file_columns for col in required_columns):
            if raise_error:
                raise ValueError(
                    f"Table does not contain required columns: {required_columns}"
                )
            return False
        return True


def _get_columns(df, required_sheets):
    given_columns = []
    if isinstance(df, dict):
        for sheet, table in df.items():
            if sheet not in required_sheets:
                continue
            given_columns.append(table.columns.tolist())
        given_columns = set(itertools.chain.from_iterable(given_columns))
    elif isinstance(df, pd.DataFrame):
        given_columns = df.columns
    elif isinstance(df, str):
        given_columns = df.split("\n")[0]
    return given_columns


def validate_columns(df, required_columns, required_sheets=[]):
    if not required_columns:
        return

    file_columns = _get_columns(df, required_sheets)

    if (
        isinstance(
            required_columns[0],
            (
                list,
                tuple,
            ),
        )
        and len(required_columns) > 1
    ):
        for rc in required_columns:
            if _columns_validator(file_columns, rc, raise_error=False):
                return
        else:
            raise ValueError(
                f"Table does not contain required columns: {required_columns}"
            )
    else:
        _columns_validator(file_columns, required_columns, raise_error=True)


def _sheets_validator(sheets, required_sheets, raise_error=True):

    common_sheets = list(set.intersection(set(sheets), set(required_sheets)))

    if sorted(required_sheets) != sorted(common_sheets):
        missing_sheets = set.difference(set(required_sheets), set(sheets))
        if raise_error:
            raise ValueError(
                f"File doesn't contain the following needed sheets: {missing_sheets}"
            )
        return False

    return True


def validate_sheets(file, required_sheets):
    """
    Raise error if required_sheets are not found in file

    required_sheets = [
        ('tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'),
        ('vInfo', 'vCPU', 'vHost', 'vCluster'),
    ]

    or

    required_sheets = 'tabvInfo', 'tabvCPU', 'tabvHost', 'tabvCluster'

    """

    if not required_sheets:
        return

    sheets = pd.ExcelFile(file).sheet_names

    # Registry service saves tuples as lists
    if (
        isinstance(required_sheets[0], tuple) or isinstance(required_sheets[0], list)
    ) and len(required_sheets) > 1:
        for rs in required_sheets:
            if _sheets_validator(sheets, rs, raise_error=False):
                return  # one validation succeded
    else:
        _sheets_validator(sheets, required_sheets, raise_error=True)


def validate_rows_number(df, min_rows_number, required_sheets=[]):
    """
    Raise error if minimum_rows_number is not satisfied
    """

    if not min_rows_number:
        return

    if isinstance(df, dict):
        for sheet, table in df.items():
            if sheet not in required_sheets:
                continue
            if table.shape[0] < min_rows_number:
                raise ValueError(
                    f"Expected {sheet} to have at least {min_rows_number} row(s)"
                )

    elif isinstance(df, pd.DataFrame):
        if df.shape[0] < min_rows_number:
            raise ValueError(
                f"Expected {sheet} to have at least {min_rows_number} row(s)"
            )
    elif isinstance(df, str):
        if df.count("\n") < min_rows_number:
            raise ValueError(
                f"Expected table to have at least {min_rows_number} row(s)"
            )
    else:
        log.error(f"Can't check min_rows_number")


def validate_filename(
    filename: str, contains: list, endswith: list = None, regex_escape: bool = True
):
    """
    Check if filename contains all needed keywords and all accepted file types
    """
    if endswith is None:
        endswith = []

    if not isinstance(filename, str):
        raise ValueError("filename must be a string")

    validate_text_contains_any(filename, contains, regex_escape)

    if endswith:
        for file_type in endswith:
            if filename.lower().endswith(file_type):
                return

        raise ValueError(
            f"Filename doesn't end with any of the specified values: {', '.join(endswith)}"
        )


class GeneralValidator:
    def __init__(
        self,
        input_object,
        required_input_type=None,
        required_sheets=[],
        required_columns=[],
        text_contains_all=[],
        text_contains_any=[],
        regex_escape=True,
        min_rows_number=0,
        header_starts_at=0,
        buffer=9000,
    ):

        self.input_object = input_object
        self.required_input_type = required_input_type
        self.required_sheets = required_sheets
        self.required_columns = required_columns
        self.text_contains_all = text_contains_all
        self.text_contains_any = text_contains_any
        self.regex_escape = regex_escape
        self.min_rows_number = min_rows_number
        self.header_starts_at = header_starts_at
        self.skip_validate_type = False
        # Making sure we don't miss characters
        self.buffer = (
            buffer
            + sum([len(c) for c in required_columns])
            + len(text_contains_all)
            + len(text_contains_any)
        )
        # Calling validation on init, raise Exception if something is wrong
        self.validate()

    def _validate_type(self):
        """
        Determine which handler to use based on input type provided
        Raise error if file/obj type is not as expected (excel/txt file, or string/stream)
        """

        if isinstance(self.input_object, str):
            if not os.path.exists(self.input_object):
                self.required_input_type = "string"
                return

        if "stream" in str(dir(self.input_object)):
            if self.required_input_type == "excel":
                self.required_input_type = "excel-stream"
                return
            else:
                self.required_input_type = "stream"
                return

        if (
            self.required_columns == []
            and self.text_contains_any
            or self.text_contains_all
        ):
            self.required_input_type = "txt"
            return

        if os.path.exists(self.input_object):

            if self.input_object.endswith(".xlsx") or self.input_object.endswith(
                ".xls"
            ):
                self.required_input_type = "excel"

            elif self.input_object.endswith(".csv"):
                self.required_input_type = "csv"

            elif self.input_object.endswith(".txt"):
                self.required_input_type = "txt"
        else:
            self.required_input_type = "string"

    def _check_required_input_type(self):
        allowed_input_types = [
            "excel",
            "csv",
            "txt",
            "string",
            "stream",
            "excel-stream",
        ]
        if not self.required_input_type:
            return
        if self.required_input_type not in allowed_input_types:
            raise ValueError(
                'Only ".xlsx", ".xls", ".csv", ".txt" files types are accepted!'
            )

    def _parse_excel_stream(self):

        self.input_object.seek(0)
        xlobj = pd.ExcelFile(BytesIO(self.input_object.stream.read()))
        sheets = xlobj.sheet_names

        if len(sheets) == 1:
            return pd.read_excel(
                xlobj, nrows=self.min_rows_number, skiprows=self.header_starts_at
            )

        dfs = {}
        for sheet in sheets:
            if sheet not in self.required_sheets:
                continue
            dfs[sheet] = pd.read_excel(
                xlobj,
                sheet_name=sheet,
                nrows=self.min_rows_number,
                skiprows=self.header_starts_at,
            )
        return dfs

    def _parse_excel(self):

        sheets = pd.ExcelFile(self.input_object).sheet_names

        if len(sheets) == 1:
            return pd.read_excel(
                self.input_object,
                nrows=self.min_rows_number,
                skiprows=self.header_starts_at,
            )

        dfs = {}
        for sheet in sheets:
            if sheet not in self.required_sheets:
                continue
            dfs[sheet] = pd.read_excel(
                self.input_object,
                sheet_name=sheet,
                nrows=self.min_rows_number,
                skiprows=self.header_starts_at,
            )

        return dfs

    def _sniff_delimiter(self):
        reader = pd.read_csv(
            self.input_object, sep=None, iterator=True, engine="python"
        )
        delimiter = reader._engine.data.dialect.delimiter
        reader.close()
        if delimiter in [",", ";"]:
            log.info(f"Sniffed delimiter '{delimiter}' for {self.input_object}")
            return delimiter
        else:
            log.warning(
                f"Sniffed illegal delimiter {delimiter} for {self.input_object}"
            )
            return ","

    def _parse_csv(self):
        df = pd.read_csv(
            self.input_object,
            nrows=self.min_rows_number,
            skiprows=self.header_starts_at,
            delimiter=self._sniff_delimiter(),
        )
        return df

    def _parse_data(self):

        if self.required_input_type == "excel-stream":
            return self._parse_excel_stream()

        if self.required_input_type == "excel":
            return self._parse_excel()

        elif self.required_input_type == "csv":
            return self._parse_csv()

        elif self.required_input_type == "txt":
            with open(self.input_object, "r", encoding="utf8", errors="ignore") as f:
                text = f.read(self.buffer)
            return text

        elif self.required_input_type == "string":
            return self.input_object

        elif self.required_input_type == "stream":
            self.input_object.seek(0)
            if self.min_rows_number:
                return self.input_object.stream.read().decode("utf8", "ignore")
            else:
                return self.input_object.stream.read(self.buffer).decode(
                    "utf8", "ignore"
                )

        else:
            raise ValueError("File contents are badly formated and cannot be read!")

    def validate(self):
        """
        When called run all validators on `input_object` parameter
        """
        self._check_required_input_type()
        self._validate_type()
        data = self._parse_data()

        validate_text_contains_all(data, self.text_contains_all, self.regex_escape)
        validate_text_contains_any(data, self.text_contains_any, self.regex_escape)
        validate_sheets(self.input_object, self.required_sheets)
        validate_columns(data, self.required_columns, self.required_sheets)
        validate_rows_number(data, self.min_rows_number, self.required_sheets)
