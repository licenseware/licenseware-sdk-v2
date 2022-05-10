import os


if os.getenv("ENVIRONMENT") == "desktop" and os.getenv("MONGOLOCAL", "false") == "true":

    from .mongitadata import (
        insert, 
        fetch, 
        update,
        delete, 
        document_count, 
        delete_collection, 
        aggregate,
        get_collection,
        distinct,
        create_collection
    ) 

    from .mongita_connection import collection

else:

    from .mongodata import (
        insert_many,
        insert, 
        fetch, 
        update,
        delete, 
        document_count, 
        delete_collection, 
        aggregate,
        get_collection,
        distinct,
        create_collection
    ) 

    from .mongo_connection import collection