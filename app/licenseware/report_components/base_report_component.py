# from app.licenseware.report_components.build_match_expression import build_match_expression


class BaseReportComponent:
    
    def __init__(
        self,
        title:str,
        component_id:str,
        component_type:str,
        path:str = None,
        order:int = None,
        
    ):
        
        self.title = title
        self.component_id = component_id
        self.component_type = component_type
        self.path = path or '/' + component_id
        self.order = order
        
        # "style_attributes": {
        #     "width": "1/3"
        # },
        # "attributes": devices_by_os.attributes_pie_chart(),
       
       
    def return_data(self, flask_request):
        raise NotImplementedError("Retrival of data for this component is not implemented")

    def return_attributes(self):
        pass


    def return_registration_payload(self):
        pass
        
        
    # def get_default_filters(self, flask_request):
        
    #     tenant_id = flask_request.headers.get('Tenantid')
    #     filters = build_match_expression(flask_request.json) if flask_request.json else None
     
    #     self.default_filters = {'tenant_id': tenant_id, 'filters': filters}
        
    
    
    
    
    
class SummaryReportComponent(BaseReportComponent):
    def __init__(
        self,
        title:str,
        component_id:str,
        component_type:str,        
    ):
        super().__init__(
            title=title, component_id=component_id, component_type=component_type
        )
        
    
        
    def get_data(self, flask_request): 
        
        tenant_id, filters = (flask_request)
        #TODO insert default filters 
        pipeline = ['mongo pipeline']
        
        return pipeline
    
    def get_attributes(self):
        return #TODO data_props function attributes
    
    def get_style_attributes(self):
        return #TODO data_props function attributes
    
        


"""
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