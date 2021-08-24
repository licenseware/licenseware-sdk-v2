from flask import Request
from app.licenseware.utils.logger import log
from app.licenseware.common.constants import envs
from app.licenseware.utils.miscellaneous import generate_id, flat_dict
from app.licenseware.report_components.build_match_expression import build_match_expression
from app.licenseware.registry_service import register_component
from app.licenseware.report_components.attributes import (
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
        self.path = path or '/' + component_id
        # We are using `generate_small_id` func to avoid component_id conflicts
        # This `component_url` is independed from the report 
        self.component_path = '/' + generate_id() + self.path
        self.component_url = envs.REPORT_COMPONENT_URL + self.component_path
        self.order = order
        self.style_attributes = style_attributes
        self.attributes = attributes
        self.registration_payload = registration_payload
        self.options = options
        
        
        
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
        
        received_filters.append({
            'field_name': 'tenant_id', 
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
        
    def get_registration_payload(self):
        
        attributes = self.set_attributes()
        if attributes: self.attributes = attributes
        
        style_attributes = self.set_style_attributes()
        if style_attributes: self.style_attributes = style_attributes
        
        return {
            "title": self.title,
            "order": self.order,
            "component_id": self.component_id,
            "path": self.path,
            "component_url": self.component_url,
            "style_attributes": self.style_attributes,
            "attributes": self.attributes,
            "component_type": self.component_type
        }
        
        
    def register_component(self):
        
        payload = self.get_registration_payload()
        
        response, status_code = register_component(**payload)
        
        if status_code not in {200, 201}:
            raise Exception("Report Component failed to register!")
        
        return response, status_code

        

        
        
         
        
"""


from marshmallow import Schema, fields

class DevicesByOs(Schema):

    operating_system_type = fields.Str(required=True, registration_payload={"visible_name": "Operating System Type", "type": "label"})
    number_of_devices = fields.Int(required=True, registration_payload={"visible_name": "Number of Devices", "type": "value"})



def attributes_pie_chart():
    return {
        "series": [
            {
                "label_description": "Operating System Type",
                "label_key": "operating_system_type"
            },
            {
                "value_description": "Number of Devices",
                "value_key": "number_of_devices"
            }
        ]
    }
10:42
device_name = fields.Str(required=True, registration_payload={"visible_name": "Device Name", "description": "The name of the device"})
10:45
from marshmallow import Schema, fields

class DevicesByOs(Schema):

    class Meta:
        render_as = ['pie', 'table']
        id = 'devices_by_os'

    operating_system_type = fields.Str(required=True, registration_payload={"visible_name": "Operating System Type", "type": "label"})
    number_of_devices = fields.Int(required=True, registration_payload={"visible_name": "Number of Devices", "type": "value"})
from marshmallow.fields import Url


class BaseReportComponent:

    def __init__(self, title, id, type, style_attributes) -> None:
        self.title = title
        self.id = id 
        self.url = id 
        self.type = type
        self.style_attributes = style_attributes

    def return_data(self, flask_request):
        pass

    def return_attributes(self):
        pass

    def return_registration_payload(self):
        return {
            "component_id": self.component_id,
            "url": self.url,
            "order": self.order,
            "style_attributes": self.style_attributes,
            "attributes": self.return_attributes,
            "title": self.title,
            "type": self.type
        }


class ODBSummary(BaseReportComponent):
    
    def __init__(self, title, style_attributes, type) -> None:
        super().__init__(title=title, id="odb-overview", style_attributes=style_attributes, type=type)

    def return_data(self, flask_request):
        #pipeline ... 
        pass

    def return_attributes(self):
        if self.type == 'summary':
            return self.return_attributes_summary()
            

    def return_attributes_summary(self):
        return  {
        "series": [
            {
                "label_description": "Version",
                "label_key": "version"
            },
            {
                "value_description": "Number of Databases",
                "value_key": "number_of_databases"
            }
        ]
    }
    
"""