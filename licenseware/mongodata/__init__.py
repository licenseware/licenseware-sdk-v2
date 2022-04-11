import os


if os.getenv("ENVIRONMENT") == "desktop":

    from .mongitadata import (
        insert, 
        fetch, 
        update,
        delete, 
        document_count, 
        delete_collection, 
        aggregate,
        get_collection,
        distinct
    ) 

    from .mongita_connection import collection

else:

    from .mongodata import (
        insert, 
        fetch, 
        update,
        delete, 
        document_count, 
        delete_collection, 
        aggregate,
        get_collection,
        distinct
    ) 

    from .mongo_connection import collection