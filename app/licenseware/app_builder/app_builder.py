




class AppBuilder:
    
    def __init__(
        self, 
        id: str, 
        name: str, 
        description: str, 
        flags: list = None, 
        **kwargs
    ):
        
        # input parameters
        self.id = id 
        self.name = name
        self.description = description
        self.flags = flags
        self.kwargs = kwargs
        
        # AppBuilder internal parameters
        self.flask_app = None
        self.restx_api = None
    

    def __call__(self):
        return self.flask_app
        
    
    
    
    def register_endpoint(self, instance):
        print(instance.__name__, "registered")
            
    def register_endpoints(self, *instances):
        for instance in instances:
            self.register_endpoint(instance)
    

    def register_uploader(self, instance):
        print(instance.__name__, "registered")
    
    
    def register_uploaders(self, *instances):
        for instance in instances:
            self.register_uploader(instance)
    
    
    def register_report(self, instance):
        print(instance.__name__, "registered")
            
        
    def register_reports(self, *instances):
        for instance in instances:
            self.register_report(instance)
            
    