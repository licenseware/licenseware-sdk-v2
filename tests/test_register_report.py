import unittest

from licenseware.registry_service import register_report

# python3 -m unittest tests/test_register_report.py


payload = {
    "data": [
        {
            "app_id": "odb_222",
            "report_id": "odb_usage_222",
            "report_name": "Oracle Database Usage Report",
            "description": "Full details on what options and packs are used and what features trigger the need for licensing. Includes OEM Managed targets and usage evidence.",
            "flags": [],
            "url": "http://localhost:5000/odb/reports/odb_usage",
            "report_components": [
                {
                    "app_id": "odb",
                    "title": "Overview",
                    "order": 1,
                    "component_id": "odb_overview_summary",
                    "url": "http://localhost:5000/odb/reports/odb_usage/odb_overview_summary",
                    "style_attributes": {"width": "1/3"},
                    "attributes": {
                        "series": [
                            {
                                "value_description": "Number of devices",
                                "value_key": "number_of_devices",
                                "icon": "ServersIcon",
                            },
                            {
                                "value_description": "Number of databases",
                                "value_key": "number_of_databases",
                                "icon": "DatabaseIconRounded",
                            },
                        ]
                    },
                    "filters": None,
                    "type": "summary",
                },
                {
                    "app_id": "odb",
                    "title": "Databases by Version",
                    "order": 2,
                    "component_id": "databases_by_version_pie",
                    "url": "http://localhost:5000/odb/reports/odb_usage/databases_by_version_pie",
                    "style_attributes": {"width": "1/3"},
                    "attributes": {
                        "series": [
                            {"label_description": "Version", "label_key": "version"},
                            {
                                "value_description": "Number of Databases",
                                "value_key": "number_of_databases",
                            },
                        ]
                    },
                    "filters": None,
                    "type": "pie",
                },
                {
                    "app_id": "odb",
                    "title": "Editions Overview",
                    "order": 3,
                    "component_id": "editions_overview_pie",
                    "url": "http://localhost:5000/odb/reports/odb_usage/editions_overview_pie",
                    "style_attributes": {"width": "1/3"},
                    "attributes": {
                        "series": [
                            {"label_description": "Edition", "label_key": "edition"},
                            {
                                "value_description": "Number of Databases",
                                "value_key": "number_of_databases",
                            },
                        ]
                    },
                    "filters": None,
                    "type": "pie",
                },
                {
                    "app_id": "odb",
                    "title": "Running Options Barv",
                    "order": 4,
                    "component_id": "running_options_barv",
                    "url": "http://localhost:5000/odb/reports/odb_usage/running_options_barv",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "series": [
                            {
                                "label_description": "Option Name",
                                "label_key": "option_name",
                            },
                            {
                                "value_description": "Number of Databases",
                                "value_key": "number_of_databases",
                            },
                        ]
                    },
                    "filters": None,
                    "type": "bar_vertical",
                },
                {
                    "app_id": "odb",
                    "title": "Oracle Databases Installed",
                    "order": 5,
                    "component_id": "oracle_databases_installed_table",
                    "url": "http://localhost:5000/odb/reports/odb_usage/oracle_databases_installed_table",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "columns": [
                            {"name": "Device Name", "prop": "device_name"},
                            {"name": "Database Name", "prop": "database_name"},
                            {"name": "Product Name", "prop": "product_name"},
                            {"name": "Product Edition", "prop": "product_edition"},
                            {"name": "Product Version", "prop": "product_version"},
                            {"name": "Full Version", "prop": "full_version"},
                            {"name": "Instance Status", "prop": "instance_status"},
                            {"name": "Application", "prop": "application"},
                            {"name": "Environment", "prop": "environment"},
                            {"name": "Source", "prop": "source"},
                        ]
                    },
                    "filters": None,
                    "type": "table",
                },
                {
                    "app_id": "odb",
                    "title": "Oracle Options Matrix",
                    "order": 6,
                    "component_id": "oracle_options_matrix",
                    "url": "http://localhost:5000/odb/reports/odb_usage/oracle_options_matrix",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "columns": [
                            {"name": "Device Name", "prop": "device_name"},
                            {"name": "Database Name", "prop": "database_name"},
                            {"name": "Active Data Guard", "prop": "active_data_guard"},
                            {
                                "name": "Advanced Analytics",
                                "prop": "advanced_analytics",
                            },
                            {
                                "name": "Advanced Compression",
                                "prop": "advanced_compression",
                            },
                            {"name": "Advanced Security", "prop": "advanced_security"},
                            {
                                "name": "Data Masking and Subsetting Pack",
                                "prop": "data_masking_and_subsetting_pack",
                            },
                            {
                                "name": "Database Lifecycle Management Pack",
                                "prop": "database_lifecycle_management_pack",
                            },
                            {"name": "Database Valut", "prop": "database_vault"},
                            {"name": "Diagnostics Pack", "prop": "diagnostics_pack"},
                            {"name": "In-Memory Database", "prop": "database_inmemory"},
                            {"name": "Label Security", "prop": "label_security"},
                            {"name": "Multitenant", "prop": "multitenant"},
                            {"name": "OLAP", "prop": "online_analytical_processing"},
                            {"name": "Partitioning", "prop": "partitioning"},
                            {"name": "RAC One Node", "prop": "rac_one_node"},
                            {
                                "name": "Real Application Clusters",
                                "prop": "real_application_clusters",
                            },
                            {
                                "name": "Real Application Testing",
                                "prop": "real_application_testing",
                            },
                            {"name": "Spatial and Graph", "prop": "spatial_and_graph"},
                            {"name": "Tuning Pack", "prop": "tuning_pack"},
                        ]
                    },
                    "filters": None,
                    "type": "table",
                },
                {
                    "app_id": "odb",
                    "title": "Options Analysis",
                    "order": 7,
                    "component_id": "options_analysis",
                    "url": "http://localhost:5000/odb/reports/odb_usage/options_analysis",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "columns": [
                            {"name": "Device Name", "prop": "device_name"},
                            {"name": "Database Name", "prop": "database_name"},
                            {"name": "Option Name", "prop": "option_name"},
                            {"name": "Final Result", "prop": "final_result"},
                            {"name": "First Usage Date", "prop": "first_usage_date"},
                            {"name": "Last Usage Date", "prop": "last_usage_date"},
                            {"name": "Other results", "prop": "other_results"},
                            {"name": "Analysis Summary", "prop": "summary"},
                            {"name": "Detailed Analysis", "prop": "detailed_analysis"},
                        ]
                    },
                    "filters": None,
                    "type": "table",
                },
                {
                    "app_id": "odb",
                    "title": "Options Usage Evidence",
                    "order": 8,
                    "component_id": "options_usage_evidence",
                    "url": "http://localhost:5000/odb/reports/odb_usage/options_usage_evidence",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "columns": [
                            {"name": "Device Name", "prop": "device_name"},
                            {"name": "Database Name", "prop": "database_name"},
                            {"name": "Database Version", "prop": "db_version"},
                            {"name": "Option Name", "prop": "option_name"},
                            {"name": "Feature Name", "prop": "feature_name"},
                            {"name": "File Name", "prop": "file_name"},
                            {"name": "Result", "prop": "result"},
                            {"name": "Licensing Notes", "prop": "note"},
                            {"name": "Evidence", "prop": "evidence"},
                        ]
                    },
                    "filters": None,
                    "type": "table",
                },
                {
                    "app_id": "odb",
                    "title": "OEM Managed Targets",
                    "order": 9,
                    "component_id": "oem_managed_targets",
                    "url": "http://localhost:5000/odb/reports/odb_usage/oem_managed_targets",
                    "style_attributes": {"width": "full"},
                    "attributes": {
                        "columns": [
                            {"name": "Device Name", "prop": "device_name"},
                            {"name": "Database Name", "prop": "database_name"},
                            {"name": "Target Type", "prop": "target_type_d"},
                            {"name": "Target Name", "prop": "target_name"},
                            {"name": "OEM Pack", "prop": "oem_pack"},
                            {"name": "Pack Label", "prop": "pack_label"},
                            {
                                "name": "Pack Access Agreed",
                                "prop": "pack_access_agreed",
                            },
                            {
                                "name": "Pack Access Agreed Date",
                                "prop": "pack_access_agreed_date",
                            },
                            {
                                "name": "Pack Access Agreed By",
                                "prop": "pack_access_agreed_by",
                            },
                        ]
                    },
                    "filters": None,
                    "type": "table",
                },
            ],
            "connected_apps": [],
            "filters": [
                {
                    "column": "device_name",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Device Name",
                },
                {
                    "column": "database_name",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Database Name",
                },
                {
                    "column": "version.edition",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Product Edition",
                },
                {
                    "column": "version.version",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Product Version",
                },
                {
                    "column": "oracle_usage.software_name",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Option Name",
                },
                {
                    "column": "oracle_usage.feature_name",
                    "allowed_filters": ["equals", "contains", "in_list"],
                    "visible_name": "Feature Name",
                },
                {
                    "column": "updated_at",
                    "allowed_filters": [
                        "equals",
                        "greater_than",
                        "greater_or_equal_to",
                        "less_than",
                        "less_or_equal_to",
                    ],
                    "visible_name": "Last Update Date",
                },
            ],
        }
    ]
}


class TestRegisterReport(unittest.TestCase):
    def test_register_uploader(self):

        data = payload["data"][0]

        data["name"] = data.pop("report_name")

        response, status_code = register_report(**data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
