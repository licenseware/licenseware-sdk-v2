




class AppBuilder:
    
    """
    Description:
    
        AppBuilder creates the base Api and common functionality for an app 
        
    Usage:
    
        from licenseware.app_builder import AppBuilder

        ifmp_app = AppBuilder(
            id = "ifmp",
            name = "Infrastructure Mapper",
            description = "Overview of devices and networks",
            flags = ['Beta']
            # + other params
        )

        ifmp_app.register_uploader(uploader_instance)
        ifmp_app.register_endpoint(endpoint_instance)
        ifmp_app.register_report(report_instance)

        app = ifmp_app()

        # where app is the Flask app instance


    """
    
    
    def __init__(self, id: str, name: str, description: str, flags: list = None, **kwargs):
        self.id = id # validate id to be only lowercase with underscores
        self.name = name
        self.description = description
        self.flags = flags
    
    
    def register_uploader(self, instance):
        print(instance.__name__, "registered")
    
    
    def register_uploaders(self, *instances):
        for instance in instances:
            self.register_uploader(instance)
    
    
    def register_endpoint(self, instance):
        print(instance.__name__, "registered")
            
    def register_endpoints(self, *instances):
        for instance in instances:
            self.register_endpoint(instance)
    
    
    def register_report(self, instance):
        print(instance.__name__, "registered")
            
        
    def register_reports(self, *instances):
        for instance in instances:
            self.register_report(instance)
            
    