import unittest

from licenseware.utils.escapehtml import escapehtml


# python3 -m unittest tests/test_escapehtml.py

class TestEscapeHtml(unittest.TestCase):


    def test_escapehtml(self):

        # String
        data = "simple string"
        escaped_data = escapehtml(data)
        assert escaped_data == data
        assert type(escaped_data) == type(data)

        # Int
        data = 1
        escaped_data = escapehtml(data)
        assert escaped_data == data
        assert type(escaped_data) == type(data)

        # Float
        data = 1.1
        escaped_data = escapehtml(data)
        assert escaped_data == data
        assert type(escaped_data) == type(data)

        # List
        data = [1.1]
        escaped_data = escapehtml(data)
        assert escaped_data == data
        assert type(escaped_data) == type(data)
        assert type(escaped_data[0]) == type(data[0])

        # Dict
        data = {
            "key": [1.1, {"keynested": {"keynestednested": ["values", 1,2,3]}}], 
            "updated_at": "2022-04-14T05:25:13.000000Z"
        }
        escaped_data = escapehtml(data)

        assert escaped_data == data
        assert type(escaped_data) == type(data)
        assert type(escaped_data['key']) == list
        assert type(escaped_data['updated_at']) == str
        assert type(escaped_data['key'][0]) == float
        assert type(escaped_data['key'][1]) == dict
        assert type(escaped_data['key'][1]["keynested"]) == dict
        assert type(escaped_data['key'][1]["keynested"]["keynestednested"]) == list
        assert type(escaped_data['key'][1]["keynested"]["keynestednested"][0]) == str
        assert type(escaped_data['key'][1]["keynested"]["keynestednested"][1]) == int

        # None
        data = None
        escaped_data = escapehtml(data)
        assert escaped_data == data

        # XSS
        data = {"logo": "<img src=x onerror=alert(3)>"}
        escaped_data = escapehtml(data)
        print(escaped_data)
        assert escaped_data != data
