import sys, os
from typing import List
from flask import send_from_directory
import importlib.resources as pkg_resources
from flask_restx import Namespace, Resource
from licenseware.decorators import failsafe
from licenseware.report_builder import ReportBuilder
from licenseware.decorators.auth_decorators import authorization_check






def create_report_resource(report: ReportBuilder):
    
    dirpath  = os.path.join(sys.path[0], "app/resources/")
    filename = report.preview_image or report.report_id + '.png'
    
    resources_path = os.path.join(dirpath, filename)
        
    if not os.path.exists(resources_path): 
        return None #exit func if image doesn't exist
                
    class ReportRegister(Resource):         
        @failsafe(fail_code=500)   
        @authorization_check
        def get(self):
            return send_from_directory(
            directory=dirpath, 
            filename=filename, 
            as_attachment=False
        )
    
    return ReportRegister
    


def get_report_image_preview_namespace(ns: Namespace, reports:List[ReportBuilder]):
    
    for report in reports:
        
        RR = create_report_resource(report)
        if RR is None: continue
        
        @ns.doc(
            description="Get report image preview image",
            responses={
                200 : "Returned image",
                403 : "Missing `Authorization` information",
                500 : "Could not return the image" 
            },
        )
        class TempReportResource(RR): ...
        
        ReportResource = type(
            report.report_id.replace("_", "").capitalize() + 'previewImage',
            (TempReportResource, ),
            {}
        )
        
        ns.add_resource(ReportResource, report.preview_image_path) 
                
    return ns
        
             
