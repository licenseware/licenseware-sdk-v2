from unittest import TestCase
from licenseware.common.constants.envs_helpers import mongo_connection_ok


# python3 -m unittest tests/test_mongo_conn.py


class TestMongoConn(TestCase):

    def test_mongo_connection_ok(self):

        mongourilist = [
            "mongodb://localhost:27017/db", #default
            "mongodb://lware:lware-secret@localhost:27017", #debug
            "mongodb://lware:lware-secret@mongo:27017", #stack
        ]

        ok = False
        for mongouri in mongourilist:
            if mongo_connection_ok(mongouri):
                ok = True
                break
                
        if not ok:
            raise Exception("No uri matched")