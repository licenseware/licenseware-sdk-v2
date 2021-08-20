import unittest
from app.licenseware.report_components.data_props import bar_vertical_chart_props


# python3 -m unittest tests/test_bar_vertical_props.py


class TestBarChartVerticalProps(unittest.TestCase):
    
    def test_table_props(self):
        
        raw_props = [
            {'xaxis_name': 'Option name', 'xaxis_machine_name': 'option_name'},
            {'yaxis_name': 'Number of databases','yaxis_machine_name': 'number_of_databases'}
        ]
        
        props = bar_vertical_chart_props(
            xaxis_machine_name="option_name", 
            yaxis_machine_name="number_of_databases"
        )

        # print(props)
        
        self.assertIn('series', props)
        self.assertListEqual(props['series'], raw_props)
        
    






