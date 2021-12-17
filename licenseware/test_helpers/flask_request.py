from licenseware.utils.logger import log



def create_mock_flask_request(
    headers:dict = None,
    args:dict = None,
    json:dict = None
):
    """
        Build an equivalent to flask request object which can be used in tests.
        TODO - files
    """
    
    class MockFlaskRequest:
        
        headers_data = {}
        args_data = {}
        json = None
        
        class headers:
            @staticmethod
            def get(val): 
                arg = MockFlaskRequest.headers_data.get(val)
                if arg is None: return None
                return str(arg)
                
        
        class args:
            @staticmethod
            def get(val):
                arg = MockFlaskRequest.args_data.get(val)
                if arg is None: return None
                return str(arg)
         
              
    MockFlaskRequest.headers_data = headers if headers is not None else {} 
    MockFlaskRequest.args_data = args if args is not None else {} 
    MockFlaskRequest.json = json
      
      
    return MockFlaskRequest
                