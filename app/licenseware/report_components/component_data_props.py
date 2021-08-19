

def attributes_table():
    return {
        'columns': [
            {
                'name': 'Number of Devices',
                'prop': 'number_of_devices'
            },
            {
                'name': 'Number of Databases',
                'prop': 'number_of_databases'
            },

        ]
    }


def attributes_summary():
    return {
        "series": [
            {
                "value_description": "Number of Devices",
                "value_key": "number_of_devices",
                "icon": "ServersIcon"
            },
            {
                "value_description": "Number of Databases",
                "value_key": "number_of_databases",
                "icon": "DatabaseIconRounded"
            }
        ]
    }



def attributes_pie_chart():
    return {
        "series": [
            {
                "label_description": "Device Type",
                "label_key": "device_type"
            },
            {
                "value_description": "Number of Devices",
                "value_key": "number_of_devices"
            }
        ]
    }
    
    
    

def attributes_bar_vertical():
    return {
        "series": [
            {
                "xaxis_description": "Option Name",
                "xaxis_key": "option_name"
            },
            {
                "yaxis_description": "Number of Databases",
                "yaxis_key": "number_of_databases"
            }
        ]
    }