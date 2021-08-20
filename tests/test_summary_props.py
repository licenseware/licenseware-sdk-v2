import unittest
from app.licenseware.report_components.data_props import summary_props


# python3 -m unittest tests/test_summary_props.py



class TestSummaryProps(unittest.TestCase):
    
    def test_summary_props(self):
        
        machine_names_icons = [
            ("number_of_devices", "ServersIcon"), 
            ("number_of_databases", "DatabaseIconRounded")
        ]
        
        props = summary_props(machine_names_icons)
        
        raw_props = [{'name': 'Number of devices', 'machine_name': 'number_of_devices', 'icon': 'ServersIcon'}, {'name': 'Number of databases', 'machine_name': 'number_of_databases', 'icon': 'DatabaseIconRounded'}]
        
        self.assertIn('series', props)
        self.assertListEqual(props['series'], raw_props)
        
    