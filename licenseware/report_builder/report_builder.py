from licenseware.common.constants.envs import envs
from licenseware.registry_service import register_report
from licenseware.report_components.build_match_expression import condition_switcher
from licenseware.report_components import BaseReportComponent
from licenseware.utils.logger import log
from typing import List






class ReportBuilder:
    """
    
    :name - report name
    :report_id - report id (will be used to construct path/route)
    :description - report data description
    :report_components - instantiated class objects from report_components
    :registrable - If True report will be registered to registry service
    :report_path - the endpoint/route on which this report is found
    :preview_image_url - the full url to a static report image
    :connected_apps - related apps which are needed to build this report
    :flags - use flags dataclass from licenseware.commun.constants
    

    """
    
    def __init__(
        self,
        name:str,
        report_id:str,
        description:str,
        report_components:list,
        registrable:bool = True,
        report_path:str = None,
        preview_image_url:str = None,
        connected_apps:list = [],
        flags:list = [],
        filters:list = []
         
    ):
         
        self.report_id = report_id
        self.name = name
        self.description = description
        self.components:List[BaseReportComponent] = report_components
        self.report_path = report_path or '/' + report_id 
        self.register_report_path = self.report_path + '/register'
        self.registrable = registrable
        self.connected_apps = connected_apps
        self.app_id = envs.APP_ID
        self.flags = flags
        self.url = envs.REPORT_URL  + self.report_path
        self.preview_image_url = preview_image_url
        
        # Needed to overwrite report_components and filters
        self.report_components = []
        self.filters = filters
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
            "url": self.url,
            "connected_apps": self.connected_apps
        }
        return payload, 200
    
    
    def register_report(self):
        return register_report(**self.reportvars)

    def register_components(self):
        
        for order, component in enumerate(self.components):
            for registered_component in self.report_components:
                if registered_component['component_id'] == component.component_id:
                    raise Exception(f"Component id '{component.component_id}' was already declared")
            
            metadata = component.get_registration_payload()
            
            metadata['order'] = metadata['order'] or order + 1
            metadata['url'] = self.url + metadata.pop('path')
            metadata['type'] = metadata.pop('component_type') 
            
            # Gathering filters from all components may cause memory overload
            # Not sure if we need to extend raport filters with all component filters
            # If we do so then in the list there should be no duplicates
            # if metadata["filters"]:
            #     self.filters.extend(metadata["filters"])
                
            self.report_components.append(metadata)
            
            
            
    def register_filters(self, filters:list):
        self.filters.extend(filters)
        

    @classmethod # same func as in base_report_component
    def build_filter(cls, column:str, allowed_filters:list, visible_name:str, validate:bool = True):
        """
            Will return a dictionary similar to the one bellow:
            
            {
                "column": "version.edition",
                "allowed_filters": [
                    "equals", "contains", "in_list"
                ],
                "visible_name": "Product Edition"
            }
            
            The dictionary build will be used to filter mongo 
            
        """
        
        if validate:
            
            if " " in column: 
                raise ValueError("Parameter `column` can't contain spaces and must be all lowercase like `device_name`")

            for f in allowed_filters:
                if f not in condition_switcher.keys():
                    raise ValueError(f"Filter {f} not in {condition_switcher.keys()}")
            
        
        return dict(
            column = column,
            allowed_filters = allowed_filters,
            visible_name = visible_name
        )
        