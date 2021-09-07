from flask import Request
from licenseware.utils.logger import log
from licenseware.common.constants import envs
from licenseware.utils.miscellaneous import flat_dict
from licenseware.report_components.build_match_expression import build_match_expression, condition_switcher
from licenseware.registry_service import register_component
from licenseware.report_components.attributes import (
    attributes_bar_vertical,
    attributes_pie,
    attributes_summary,
    attributes_table
)


component_attributes_funcs = {
    'bar_vertical':attributes_bar_vertical,
    'pie': attributes_pie,
    'summary': attributes_summary,
    'table': attributes_table
}



class BaseReportComponent:
    
    def __init__(
        self,
        title:str,
        component_id:str,
        component_type:str,
        filters:list = None,
        path:str = None,
        order:int = None,
        style_attributes:dict = None,
        attributes:dict = None,
        registration_payload:dict = None,
        **options
    ):
        
        self.title = title
        self.component_id = component_id
        self.component_type = component_type
        self.filters = filters
        self.path = path or '/' + component_id
        self.component_path = '/' + self.path
        self.url = envs.REPORT_COMPONENT_URL + self.component_path
        self.order = order
        self.style_attributes = style_attributes
        self.attributes = attributes
        self.registration_payload = registration_payload
        self.options = options
        
        
    def build_filter(self, column:str, allowed_filters:list, visible_name:str, validate:bool = True):
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
        
        
        
        
        
    def build_attributes(self, *args, **kwargs):
        """
            See `report_components.attributes` functions for more info
        """
        return component_attributes_funcs[self.component_type](*args, **kwargs)


    def build_style_attributes(self, *args, **kwargs):
        """
            See `report_components.style_attributes` dataclass for more info
        """
        return flat_dict(*args, **kwargs)
    
    
    def get_mongo_match_filters(self, flask_request):
        """
            Create a mongo `$match` filter with tenant_id and filters sent from frontend 
        """
        
        received_filters = flask_request.json or []
        
        # Inserting filter by tenant_id
        received_filters.insert(0, {
            'column': 'tenant_id', 
            'filter_type': 'equals', 
            'filter_value': flask_request.headers.get('Tenantid')
        })
            
        filters = build_match_expression(received_filters)
        
        return filters
        
        
    def get_data(self, flask_request: Request):
        """ 
        Synopsis:
        
        match_filters = self.get_mongo_match_filters(flask_request)
                
        pipeline = [
            custom pipeline
        ]
        
        pipeline.insert(0, match_filters)
        
        results = ['mongo pipeline result'] //ex: mongodata.aggregate(pipeline, collection='Data')
        
        return results
            
        """
        raise NotImplementedError("Retrival of data for this component is not implemented")


    def set_attributes(self):
        raise NotImplementedError("Please overwrite method `set_attributes`")
    
    def set_style_attributes(self):
        raise NotImplementedError("Please overwrite method `set_style_attributes`")
    
    def set_allowed_filters(self):
        log.warning("Component filters not set")
        # raise NotImplementedError("Please overwrite method `set_allowed_filters`")
    
    def get_registration_payload(self):
        
        if not self.attributes:
            attributes = self.set_attributes()
            if attributes: self.attributes = attributes
        
        if not self.style_attributes: 
            style_attributes = self.set_style_attributes()
            if style_attributes: self.style_attributes = style_attributes
        
        if not self.filters:
            allowed_filters = self.set_allowed_filters()
            if allowed_filters: self.filters = allowed_filters
        
        return {
            "title": self.title,
            "order": self.order,
            "component_id": self.component_id,
            "path": self.path,
            "url": self.url,
            "style_attributes": self.style_attributes,
            "attributes": self.attributes,
            "component_type": self.component_type,
            "filters": self.filters
        }
        
        
    def register_component(self):
        
        payload = self.get_registration_payload()
        
        response, status_code = register_component(**payload)
        
        if status_code not in {200, 201}:
            raise Exception("Report Component failed to register!")
        
        return response, status_code

        

        
        