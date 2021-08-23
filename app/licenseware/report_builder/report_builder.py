from app.licenseware.common.constants.envs import envs
from app.licenseware.registry_service import register_report
from app.licenseware.utils.logger import log




class ReportBuilder:
    """
    
    :name - report name
    :report_id - report id (will be used to construct path/route)
    :description - report data description
    :report_components - instantiated class objects from report_components
    :report_path - the endpoint/route on which this report is found
    :connected_apps - related apps which are needed to build this report
    :flags - use flags dataclass from licenseware.commun.constants
    

    """
    
    def __init__(
        self,
        name:str,
        report_id:str,
        description:str,
        report_components:list,
        report_path:str = None,
        connected_apps:list = [],
        flags:list = [],
        filters:list = []
         
    ):
        self.name = name
        self.report_id = report_id
        self.description = description
        self.components = report_components
        self.report_path = report_path or '/' + report_id 
        self.register_report_path = self.report_path + '/register'
        self.connected_apps = connected_apps
        self.app_id = envs.APP_ID
        self.flags = flags
        self.filters = filters
        self.report_url = envs.REPORT_URL  + self.report_path
        
        # Needed to overwrite report_components
        self.report_components = []
        self.register_components()
        
        self.reportvars = vars(self)
     
     
    def return_json_payload(self):
        payload = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "report_name": self.name,
            "description": self.description,
            "flags": self.flags,
            "report_components": self.report_components,
            "filters": self.filters,
            "url": self.report_url,
            "connected_apps": self.connected_apps
        }
        return payload, 200
    
    
    def register_report(self):
        return register_report(**self.reportvars)


    def register_components(self):
        
        for order, component in enumerate(self.components):
            for registered_component in self.report_components:
                if registered_component.component_id == component.component_id:
                    raise Exception(f"Component id '{component.component_id}' was already declared")
            
            metadata = component.get_component_metadata()
            
            json_metadata = {
                'title': metadata['title'],
                'order': metadata['order'] or order + 1,
                'url': self.report_url + metadata['path'],
                'component_id': metadata['component_id'],
                'icon': metadata['main_icon'],
                'type': metadata['component_type'],
                'style_attributes': metadata['style_props'],
                'attributes': metadata['data_props'],
            }
            
            self.report_components.append(json_metadata)
            
        
