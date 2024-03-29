import unittest

from main import App, app

from licenseware.common.constants import envs
from licenseware.report_components import BaseReportComponent
from licenseware.utils.logger import log

from . import headers

# python3 -m unittest tests/test_download_as_url.py


class TestDownloadAs(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        self.app = app.test_client()

    def test_report_component_urls(self):

        for r in App.report_components:

            r: BaseReportComponent

            url = envs.APP_PATH + envs.REPORT_COMPONENT_PATH + r.component_path

            response = self.app.get(
                url, query_string={"download_as": "json"}, headers=headers
            )

            log.warning(url)
            log.debug(response.data)

        #     report_component_metadata[r.component_id] = response.json

    # def test_reports_urls(self):

    #     reports_metadata = []
    #     report_ids = []
    #     for r in App.reports:

    #         r:ReportBuilder

    #         url = envs.APP_PATH + envs.REPORT_PATH + r.report_path
    #         response = self.app.get(
    #             url,
    #             headers = headers
    #         )
    #         reports_metadata.append(response.json)
    #         report_ids.append(r.report_id)

    #     for metadata in reports_metadata:
    #         # log.warning(metadata)
    #         self.assertEqual(metadata['app_id'], envs.APP_ID)
    #         self.assertIn(metadata['report_id'], report_ids)
