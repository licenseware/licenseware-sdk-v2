# Conventions over configuration


## APP description

Each APP is reponsible for:
- processing one or more files aka `uploaders`;
- returning based on available proccesed data one or more `reports`;


## Basic app structure

```bash
APP
├── common
├── endpoints
├── reports
├── uploaders
└── utils
```

- `common`,`utils` : common functionality;
- `endpoints` : custom specific routes out of scope for `reports` and `uploaders`;
- `reports`   : data aggregators for a specific report;
- `uploaders` : processing file handlers responsible for getting data into database;


## Extended app structure

```bash
APP
├── common
│   └── __init__.py
├── endpoints
│   ├── custom_endpoint_name
│   │   ├── controllers
│   │   ├── serializers
│   │   └── services
│   └── __init__.py
├── __init__.py
├── reports
│   ├── __init__.py
│   ├── report_consolidated
│   │   └── __init__.py
│   └── report_name_x
│       └── __init__.py
├── uploaders
│   ├── __init__.py
│   ├── power_cli
│   │   ├── controllers
│   │   ├── __init__.py
│   │   ├── serializers
│   │   ├── services
│   │   └── workers
│   └── rv_tools
│       ├── controllers
│       ├── __init__.py
│       ├── serializers
│       ├── services
│       └── workers
└── utils
    └── __init__.py
```



https://umongo.readthedocs.io/en/latest/
https://umongo.readthedocs.io/en/latest/userguide.html


# REPORTS


history_report = ReportBuilder(
    id = 'history_report',
    name = 'History Report',
    description = 'History of actions made on ifmp app',
    connected_apps = ['odb'],
    flags = ['Beta'],
    # + other params
)


summary_component = ReportComponents.SummaryComponent(
    # we can generate component id from title (urls are namespaced)
    title = "Overview",  
    # will generate atributes + series
    attributes = [
        {"name": "Devices Analyzed", "icon": icons.device_icon},
        {"name": "Files Analyzed", "icon": icons.file_icon}, 
    ],
    data_method=fetch_summary_data
)

table_component = "similar to SummaryComponent"

#Single component
history_report.register_component(summary_component)
#Multiple components order defined by their positions
history_report.register_components(summary_component, table_component)
 


ifmp_app.register_report(history_report)


# Attrs for ifmp_app

ifmp_app.restx_api
ifmp_app.flask_app



# CLI TOOL for generating boilerplate code

# > licenseware new uploader uploader_name (will generate boilerplate code for an uploader)
# > licenseware new report report_name (will generate boilerplate code for a report)
# > licenseware new endpoint endpoint_name (will generate boilerplate code for an endpoint)


```