import unittest
from licenseware.report_components import BaseReportComponent
from licenseware.utils.logger import log
from licenseware.report_components.style_attributes import styles
from licenseware.common.constants import icons, filters
from . import tenant_id



# python3 -m unittest tests/test_report_components.py


fe_filters = [
    {
        'column': "name", 
        'filter_type': "equals", 
        'filter_value': "the device name"
    }
]


# Simulating a flask request object
class flask_request:
    
    json = fe_filters
        
    class headers:
        
        @classmethod
        def get(cls, tenant_id_param):
            assert tenant_id_param == "Tenantid"
            return tenant_id
            
         


class TestReportComponents(unittest.TestCase):
    
    def test_report_component_creation(self):
        
        class VirtualOverview(BaseReportComponent):
            
            def __init__(
                self, 
                title: str, 
                component_id: str, 
                component_type: str
            ):
                self.title = title
                self.component_id = component_id
                self.component_type = component_type
                
                super().__init__(**vars(self))
                
                
            def get_data(self, flask_request):
                
                match_filters = self.get_mongo_match_filters(flask_request)
                
                # log.info(match_filters)

                return ['mongo pipeline result']
            
            
            def set_attributes(self):
                
                # Short hand based on value_key
                # See based on component type funcs from: licenseware.report_components.attributes
                value_key_and_icon = [
                    ("number_of_devices", icons.SERVERS), 
                    ("number_of_databases", icons.DATABASE_ROUNDED)
                ]
    
                # Set values straight to self.attributes
                self.attributes = self.build_attributes(value_key_and_icon)
                
                
                # Or raw dict (same results are achived using the method up)
                
                attributes = {'series': [
                    {
                        'value_description': 'Number of devices',
                        'value_key': 'number_of_devices',
                        'icon': 'ServersIcon'
                    },
                    {
                        'value_description': 'Number of databases',
                        'value_key': 'number_of_databases',
                        'icon': 'DatabaseIconRounded'
                    }
                ]}
                
                # You can also return attributes
                return attributes
                
                
            def set_style_attributes(self):
                
                # You can set a dictionary directly or return a dict like bellow
                self.style_attributes = {
                    'width': '1/3'
                }
                
                # or import `style_attributes` dataclass
                # from licenseware.report_components.style_attributes import style_attributes as styles
                style_attributes = self.build_style_attributes([
                    styles.WIDTH_ONE_THIRD
                    #etc
                ])
                
                return style_attributes
                
                    
            def set_allowed_filters(self):
                # Provide a list of allowed filters for this component
                return [
                    # You can use the build_filter method
                    self.build_filter(
                        column="device_name", 
                        allowed_filters=[
                            filters.EQUALS, filters.CONTAINS, filters.IN_LIST
                        ], 
                        visible_name="Device Name", 
                        # validate:bool = True # This will check field_name and allowed_filters
                    ),
                    # or you can create the dictionary like bellow (disadvantage no autocomplete, no checks)
                    {
                        "column": "database_name",
                        "allowed_filters": [
                            "equals", "contains", "in_list"
                        ],
                        "visible_name": "Database Name"
                    }
                
                ]
                

                
                
                
        
        virtual_overview = VirtualOverview(
            title="Overview",
            component_id="virtual_overview",
            component_type='summary'
        )
        
        
        match_filters = virtual_overview.get_mongo_match_filters(flask_request)
        
        self.assertDictEqual(match_filters, {'$match': {'name': 'the device name', 'tenant_id': '3d1fdc6b-04bc-44c8-ae7c-5fa5b9122f1a'}})
        
        # data method
        data = virtual_overview.get_data(flask_request)
        
        self.assertEqual(data, ['mongo pipeline result'])
        
        # payload registration
        registration_payload = virtual_overview.get_registration_payload()
        
        self.assertEqual(registration_payload['component_id'], "virtual_overview")
        self.assertEqual(registration_payload['path'], '/' + "virtual_overview")
        self.assertEqual(registration_payload['style_attributes'], {'width': '1/3'})
        self.assertEqual(registration_payload['attributes']['series'], [{'value_description': 'Number of devices', 'value_key': 'number_of_devices', 'icon': 'ServersIcon'}, {'value_description': 'Number of databases', 'value_key': 'number_of_databases', 'icon': 'DatabaseIconRounded'}])
        
        # register component to registry service
        response, status_code = virtual_overview.register_component()
        self.assertEqual(status_code, 200)
        
    
        
        