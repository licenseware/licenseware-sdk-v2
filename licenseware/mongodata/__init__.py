import os

if os.getenv("ENVIRONMENT") == "desktop" and os.getenv("MONGOLOCAL", "false") == "true":

    from .mongita_connection import collection
    from .mongitadata import (
        aggregate,
        create_collection,
        delete,
        delete_collection,
        distinct,
        document_count,
        fetch,
        get_collection,
        insert,
        update,
    )

else:

    from .mongo_connection import collection
    from .mongodata import (
        aggregate,
        create_collection,
        delete,
        delete_collection,
        distinct,
        document_count,
        fetch,
        get_collection,
        insert,
        insert_many,
        update,
    )
