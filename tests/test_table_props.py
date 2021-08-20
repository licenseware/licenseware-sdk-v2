import unittest
from app.licenseware.report_components.data_props import table_props


# python3 -m unittest tests/test_table_props.py


class TestTableProps(unittest.TestCase):
    
    def test_table_props(self):
        
        machine_names = ['number_of_devices', 'number_of_databases']
        raw_props = [
            {'name': 'Number of devices', 'machine_name': 'number_of_devices'}, 
            {'name': 'Number of databases', 'machine_name': 'number_of_databases'}
        ]
        
        
        props = table_props(machine_names)
        
        # print(props)
        
        self.assertIn('columns', props)
        self.assertListEqual(props['columns'], raw_props)
        
    