from flask import Request
from licenseware import mongodata
from licenseware.common.constants import envs
from licenseware.report_builder import ReportBuilder
from licenseware.utils.dramatiq_redis_broker import broker
from licenseware.utils.logger import log

#TODO in progress

class ReportSnapshot:
    
    def __init__(self, report: ReportBuilder, flask_request:Request):
        self.report = report
        self.request = flask_request
        self.tenant_id = flask_request.headers.get('Tenantid')


    def get_report_metadata(self):
        """ 
            Get report metadata and fill report components with data 
        """
        
        report_metadata, status_code = self.report.return_json_payload()
        
        rcomponents = []
        for comp in self.report.components:
            comp_payload = comp.get_registration_payload()
            comp_payload['component_data'] = comp.get_data(self.request)
            rcomponents.append(comp_payload)
        
        report_metadata['report_components'] = rcomponents
        
        return report_metadata


    def snapshot(self):
        
        self.create_report_snapshot.send()
        

    @broker.actor(
        max_retries=0, 
        queue_name=envs.QUEUE_NAME
    )
    def create_report_snapshot(self):
        
        report_metadata = self.get_report_metadata()
        
        
        
        
        


    


