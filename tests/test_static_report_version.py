import unittest


# python3 -m unittest tests/test_static_report_version.py

class TestStaticReportVersion(unittest.TestCase):

    def test_static_report_version(self):
        pass
    

    

report_metdata = {
  "app_id": "ifmp-service",
  "report_id": "device_details_report",
  "name": "Device Details",
  "description": "This report collects all the device information captured during processing. Use this information to understand the calculation results or easily export and plug this data into your analysis tool.",
  "flags": [],
  "report_components": [
    {
      "app_id": "ifmp-service",
      "title": "Devices by OS and Type",
      "order": 1,
      "component_id": "devices_by_os_and_type",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/devices_by_os_and_type",
      "public_url": "http://localhost/ifmp/report-components/devices_by_os_and_type/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "header_columns": [
          {
            "label_description": "Operating System",
            "label_key": "operating_system",
            "icon": "ServersIcon"
          },
          {
            "value_description": "Number of Devices",
            "value_key": "number_of_devices"
          }
        ],
        "detail_columns": [
          {
            "label_description": "Device Type",
            "label_key": "devices_by_type.device_type"
          },
          {
            "value_description": "Number of Devices",
            "value_key": "devices_by_type.number_of_devices"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "detailed_summary"
    },
    {
      "app_id": "ifmp-service",
      "title": "Aix Lpar Devices",
      "order": 2,
      "component_id": "aix_lpar_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/aix_lpar_devices",
      "public_url": "http://localhost/ifmp/report-components/aix_lpar_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Physical Serial Number",
            "prop": "physical_serial_number",
            "type": "string"
          },
          {
            "name": "Pool Id",
            "prop": "pool_id",
            "type": "string"
          },
          {
            "name": "Online Virtual Cpu",
            "prop": "online_virtual_cpu",
            "type": "number"
          },
          {
            "name": "Minimum Virtual Cpu",
            "prop": "minimum_virtual_cpu",
            "type": "number"
          },
          {
            "name": "Entitled Capacity",
            "prop": "entitled_capacity",
            "type": "number"
          },
          {
            "name": "Dedicated",
            "prop": "dedicated",
            "type": "bool"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "Maximum Physical Cpu",
            "prop": "maximum_physical_cpu",
            "type": "number"
          },
          {
            "name": "Active Cpu In Physical Device",
            "prop": "active_cpu_in_physical_device",
            "type": "number"
          },
          {
            "name": "Active Cpu In Pool",
            "prop": "active_cpu_in_pool",
            "type": "number"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Aix Pool Devices",
      "order": 3,
      "component_id": "aix_pool_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/aix_pool_devices",
      "public_url": "http://localhost/ifmp/report-components/aix_pool_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "# of LPARs Running",
            "prop": "number_of_lpars",
            "type": "number"
          },
          {
            "name": "Physical Serial Number",
            "prop": "physical_serial_number",
            "type": "string"
          },
          {
            "name": "Pool Id",
            "prop": "pool_id",
            "type": "string"
          },
          {
            "name": "Maximum Physical Cpu",
            "prop": "maximum_physical_cpu",
            "type": "number"
          },
          {
            "name": "Active Cpu In Physical Device",
            "prop": "active_cpu_in_physical_device",
            "type": "number"
          },
          {
            "name": "Active Cpu In Pool",
            "prop": "active_cpu_in_pool",
            "type": "number"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Aix Physical Devices",
      "order": 4,
      "component_id": "aix_physical_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/aix_physical_devices",
      "public_url": "http://localhost/ifmp/report-components/aix_physical_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "# of Pools Running",
            "prop": "number_of_pools",
            "type": "number"
          },
          {
            "name": "Physical Serial Number",
            "prop": "physical_serial_number",
            "type": "string"
          },
          {
            "name": "Maximum Physical Cpu",
            "prop": "maximum_physical_cpu",
            "type": "number"
          },
          {
            "name": "Active Cpu In Physical Device",
            "prop": "active_cpu_in_physical_device",
            "type": "number"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Solaris Zones",
      "order": 5,
      "component_id": "solaris_zones",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/solaris_zones",
      "public_url": "http://localhost/ifmp/report-components/solaris_zones/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "State",
            "prop": "state",
            "type": "string"
          },
          {
            "name": "Pool Id",
            "prop": "pool_id",
            "type": "string"
          },
          {
            "name": "Pool Pset Name",
            "prop": "pset_name",
            "type": "string"
          },
          {
            "name": "Pool Pset Max",
            "prop": "pool_pset_max",
            "type": "number"
          },
          {
            "name": "Pool Pset Size",
            "prop": "pset_size",
            "type": "number"
          },
          {
            "name": "Global Zone",
            "prop": "global_zone",
            "type": "bool"
          },
          {
            "name": "Global Zone Name",
            "prop": "global_zone_name",
            "type": "string"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Solaris Cpu Pools",
      "order": 6,
      "component_id": "solaris_cpu_pools",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/solaris_cpu_pools",
      "public_url": "http://localhost/ifmp/report-components/solaris_cpu_pools/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "State",
            "prop": "state",
            "type": "string"
          },
          {
            "name": "# of Zones Running",
            "prop": "number_of_zones",
            "type": "number"
          },
          {
            "name": "Pool Id",
            "prop": "pool_id",
            "type": "string"
          },
          {
            "name": "Pool Pset Name",
            "prop": "pset_name",
            "type": "string"
          },
          {
            "name": "Pool Pset Max",
            "prop": "pool_pset_max",
            "type": "number"
          },
          {
            "name": "Pool Pset Size",
            "prop": "pset_size",
            "type": "number"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Solaris Domains",
      "order": 7,
      "component_id": "solaris_domains",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/solaris_domains",
      "public_url": "http://localhost/ifmp/report-components/solaris_domains/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "# of Devices Running",
            "prop": "number_of_partitions",
            "type": "number"
          },
          {
            "name": "Primary Domain",
            "prop": "primary_domain",
            "type": "bool"
          },
          {
            "name": "Primary Domain Name",
            "prop": "primary_domain_name",
            "type": "string"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Solaris Physical Devices",
      "order": 8,
      "component_id": "solaris_physical_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/solaris_physical_devices",
      "public_url": "http://localhost/ifmp/report-components/solaris_physical_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "# of Devices Running",
            "prop": "number_of_partitions",
            "type": "number"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Standalone Devices",
      "order": 9,
      "component_id": "standalone_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/standalone_devices",
      "public_url": "http://localhost/ifmp/report-components/standalone_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Virtualization Clusters",
      "order": 10,
      "component_id": "virtualization_clusters",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/virtualization_clusters",
      "public_url": "http://localhost/ifmp/report-components/virtualization_clusters/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Cluster Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "# of Cluster Members",
            "prop": "number_of_cluster_members",
            "type": "number"
          },
          {
            "name": "Cluster Members",
            "prop": "cluster_members",
            "type": "json"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Total Cores in Cluster Members",
            "prop": "total_cores_in_scanned_cluster_members",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Physical Hosts",
      "order": 11,
      "component_id": "physical_hosts",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/physical_hosts",
      "public_url": "http://localhost/ifmp/report-components/physical_hosts/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Cluster Name",
            "prop": "cluster_name",
            "type": "string"
          },
          {
            "name": "# of VMs Running",
            "prop": "number_of_vms",
            "type": "number"
          },
          {
            "name": "Running VMs",
            "prop": "running_vms",
            "type": "json"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Virtual Devices",
      "order": 12,
      "component_id": "virtual_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/virtual_devices",
      "public_url": "http://localhost/ifmp/report-components/virtual_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "Physical Host Name",
            "prop": "physical_host",
            "type": "string"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Ovm Physical Devices",
      "order": 13,
      "component_id": "ovm_physical_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/ovm_physical_devices",
      "public_url": "http://localhost/ifmp/report-components/ovm_physical_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "# of Hosted VMs",
            "prop": "number_of_vms",
            "type": "number"
          },
          {
            "name": "Hosted VMs",
            "prop": "hosted_vms",
            "type": "json"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Ovm Virtual Devices",
      "order": 14,
      "component_id": "ovm_virtual_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/ovm_virtual_devices",
      "public_url": "http://localhost/ifmp/report-components/ovm_virtual_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "Host Device Name",
            "prop": "host_device_name",
            "type": "string"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Ovm Id",
            "prop": "ovm_id",
            "type": "string"
          },
          {
            "name": "Ovm Description",
            "prop": "ovm_description",
            "type": "string"
          },
          {
            "name": "Cpu Affinity Enabled",
            "prop": "cpu_affinity_enabled",
            "type": "string"
          },
          {
            "name": "Affinity Ovm Cpu Id",
            "prop": "affinity_ovm_cpu_id",
            "type": "string"
          },
          {
            "name": "Affinity Ovm Cpu",
            "prop": "affinity_ovm_cpu",
            "type": "string"
          },
          {
            "name": "Affinity Ovm Vcpu",
            "prop": "affinity_ovm_vcpu",
            "type": "number"
          },
          {
            "name": "Ovm Vcpus",
            "prop": "ovm_vcpus",
            "type": "number"
          },
          {
            "name": "Ovm Cpu Cap",
            "prop": "ovm_cpu_cap",
            "type": "number"
          },
          {
            "name": "Ovm Max Vcpus",
            "prop": "ovm_max_vcpus",
            "type": "number"
          },
          {
            "name": "Affinity Ovm Cpu Affinity",
            "prop": "affinity_ovm_cpu_affinity",
            "type": "string"
          },
          {
            "name": "Ovm High Availability",
            "prop": "ovm_high_availability",
            "type": "string"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "string"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    },
    {
      "app_id": "ifmp-service",
      "title": "Hpux Devices",
      "order": 15,
      "component_id": "hpux_devices",
      "description": None,
      "url": "http://localhost/ifmp/reports/device_details_report/hpux_devices",
      "public_url": "http://localhost/ifmp/report-components/hpux_devices/public",
      "style_attributes": {
        "width": "full"
      },
      "attributes": {
        "columns": [
          {
            "name": "Device Name",
            "prop": "device_name",
            "type": "string"
          },
          {
            "name": "Device Type",
            "prop": "device_type_description",
            "type": "string"
          },
          {
            "name": "Capped",
            "prop": "capped",
            "type": "bool"
          },
          {
            "name": "Total Number Of Processors",
            "prop": "total_number_of_processors",
            "type": "number"
          },
          {
            "name": "Total Number Of Cores",
            "prop": "total_number_of_cores",
            "type": "number"
          },
          {
            "name": "Total Number Of Threads",
            "prop": "total_number_of_threads",
            "type": "number"
          },
          {
            "name": "Cpu Model",
            "prop": "cpu_model",
            "type": "string"
          },
          {
            "name": "Oracle Core Factor",
            "prop": "oracle_core_factor",
            "type": "number"
          },
          {
            "name": "Virtualization Type",
            "prop": "virtualization_type",
            "type": "string"
          },
          {
            "name": "Operating System Type",
            "prop": "operating_system_type",
            "type": "string"
          },
          {
            "name": "Manufacturer",
            "prop": "manufacturer",
            "type": "string"
          },
          {
            "name": "Model",
            "prop": "model",
            "type": "string"
          },
          {
            "name": "Raw Data",
            "prop": "raw_data",
            "type": "json"
          }
        ]
      },
      "filters": [
        {
          "column": "name",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Name",
          "column_type": "string"
        },
        {
          "column": "capped",
          "allowed_filters": [
            "equals"
          ],
          "visible_name": "Capped",
          "allowed_values": [
            True,
            False
          ],
          "column_type": "string"
        },
        {
          "column": "device_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Device Type",
          "allowed_values": [
            "Virtual",
            "Pool",
            "Domain",
            "Physical",
            "Cluster"
          ],
          "column_type": "string"
        },
        {
          "column": "virtualization_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Virtualization Type",
          "allowed_values": [
            "Solaris",
            "VMWare",
            "OracleVM",
            "AIX",
            "HP-UX",
            "Hyper-V",
            "Other"
          ],
          "column_type": "string"
        },
        {
          "column": "operating_system_type",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Type",
          "column_type": "string"
        },
        {
          "column": "operating_system_caption",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Operating System Caption",
          "column_type": "string"
        },
        {
          "column": "manufacturer",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Manufacturer",
          "column_type": "string"
        },
        {
          "column": "model",
          "allowed_filters": [
            "equals",
            "contains",
            "in_list"
          ],
          "visible_name": "Model",
          "column_type": "string"
        },
        {
          "column": "total_number_of_processors",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Processors",
          "column_type": "number"
        },
        {
          "column": "total_number_of_cores",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Cores",
          "column_type": "number"
        },
        {
          "column": "total_number_of_threads",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Total Number of Threads",
          "column_type": "number"
        },
        {
          "column": "oracle_core_factor",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Oracle Core Factor",
          "column_type": "number"
        },
        {
          "column": "updated_at",
          "allowed_filters": [
            "equals",
            "greater_than",
            "greater_or_equal_to",
            "less_than",
            "less_or_equal_to"
          ],
          "visible_name": "Last Update Date",
          "column_type": "date"
        }
      ],
      "type": "table"
    }
  ],
  "filters": [
    {
      "column": "name",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Device Name",
      "column_type": "string"
    },
    {
      "column": "capped",
      "allowed_filters": [
        "equals"
      ],
      "visible_name": "Capped",
      "allowed_values": [
        True,
        False
      ],
      "column_type": "string"
    },
    {
      "column": "device_type",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Device Type",
      "allowed_values": [
        "Virtual",
        "Pool",
        "Domain",
        "Physical",
        "Cluster"
      ],
      "column_type": "string"
    },
    {
      "column": "virtualization_type",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Virtualization Type",
      "allowed_values": [
        "Solaris",
        "VMWare",
        "OracleVM",
        "AIX",
        "HP-UX",
        "Hyper-V",
        "Other"
      ],
      "column_type": "string"
    },
    {
      "column": "operating_system_type",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Operating System Type",
      "column_type": "string"
    },
    {
      "column": "operating_system_caption",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Operating System Caption",
      "column_type": "string"
    },
    {
      "column": "manufacturer",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Manufacturer",
      "column_type": "string"
    },
    {
      "column": "model",
      "allowed_filters": [
        "equals",
        "contains",
        "in_list"
      ],
      "visible_name": "Model",
      "column_type": "string"
    },
    {
      "column": "total_number_of_processors",
      "allowed_filters": [
        "equals",
        "greater_than",
        "greater_or_equal_to",
        "less_than",
        "less_or_equal_to"
      ],
      "visible_name": "Total Number of Processors",
      "column_type": "number"
    },
    {
      "column": "total_number_of_cores",
      "allowed_filters": [
        "equals",
        "greater_than",
        "greater_or_equal_to",
        "less_than",
        "less_or_equal_to"
      ],
      "visible_name": "Total Number of Cores",
      "column_type": "number"
    },
    {
      "column": "total_number_of_threads",
      "allowed_filters": [
        "equals",
        "greater_than",
        "greater_or_equal_to",
        "less_than",
        "less_or_equal_to"
      ],
      "visible_name": "Total Number of Threads",
      "column_type": "number"
    },
    {
      "column": "oracle_core_factor",
      "allowed_filters": [
        "equals",
        "greater_than",
        "greater_or_equal_to",
        "less_than",
        "less_or_equal_to"
      ],
      "visible_name": "Oracle Core Factor",
      "column_type": "number"
    },
    {
      "column": "updated_at",
      "allowed_filters": [
        "equals",
        "greater_than",
        "greater_or_equal_to",
        "less_than",
        "less_or_equal_to"
      ],
      "visible_name": "Last Update Date",
      "column_type": "date"
    }
  ],
  "url": "http://localhost/ifmp/reports/device_details_report",
  "public_url": "http://localhost/ifmp/reports/device_details_report/public",
  "preview_image_url": "http://localhost/ifmp/reports/device_details_report/preview_image",
  "preview_image_dark_url": "http://localhost/ifmp/reports/device_details_report/preview_image_dark",
  "connected_apps": [
    "ifmp-service"
  ]
}