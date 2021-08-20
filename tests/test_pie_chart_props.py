import unittest
from app.licenseware.report_components.data_props import pie_chart_props


# python3 -m unittest tests/test_pie_chart_props.py



class TestPieChartProps(unittest.TestCase):
    
    def test_pie_chart_props(self):
        
        machine_names = ["device_type", "number_of_devices"]
        raw_props = [
            {'name': 'Device type', 'machine_name': 'device_type'},
            {'name': 'Number of devices', 'machine_name': 'number_of_devices'}
        ]
        
        
        props = pie_chart_props(machine_names)
        
        # print(props)
        
        self.assertIn('series', props)
        self.assertListEqual(props['series'], raw_props)
        
