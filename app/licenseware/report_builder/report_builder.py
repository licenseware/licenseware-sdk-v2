



class ReportBuilder:
    
    def __init__(
        self,
        name:str,
        report_id:str,
        description:str,
        report_path:str = None,
         
    ):
        self.name = name
        self.report_id = report_id
        self.description = description
        self.report_path = report_path or '/' + report_id 
        # When report path(url) is accesed get a list of component metadata
        # Component metadata holds the ui component type and a route which when accessed fills that ui component with data
        # An ui component can be reprezented in the front-end as a Pie Chart, Bar Chart a Table or other custom ui element
        
        
    def register_component(self, report_component):
        pass
    
    def register_report(self):
        pass