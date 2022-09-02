"""

Usage:

- Import from repository the `Database` class
- Provide the connection url to database and the customized marshmallow schema to `Database`
- Once instantiated all will have the same interface to db


```py


from repository import RepoDb
from marshmallow import Schema, fields



class UserSchema(Schema):
    name = fields.String()
    email = fields.String()


# You can use mongodb or postgresdb 
# All their specific features will be added on marshmallow schema


repo = RepoDb(db_url="mongodb://localhost:27017/db", schema=UserSchema)

repo.db.fetch()
repo.db.insert()
repo.db.update()
repo.db.delete()


# or 
# Notice we added `db` at the end to skip doing repo.db.fetch()

repo = RepoDb(db_url="postgresql://localhost:5432/db", schema=UserSchema).db

repo.fetch()
repo.insert()
repo.update()
repo.delete()

```

# or

```py

from repository.mongo import MongoRepository
from repository.postgres import PostgresRepository


repo = MongoRepository(db_url="mongodb://localhost:27017/db", schema=UserSchema)

repo.fetch()
repo.insert()
repo.update()
repo.delete()


```



"""

from marshmallow import Schema

from licenseware.repository.mongo.mongo_repository import MongoRepository
from licenseware.repository.postgres.postgres_migrations import PostgresMigrations
from licenseware.repository.postgres.postgres_repository import PostgresRepository


class RepoDb:
    def __init__(self, db_url: str, schema: Schema):

        if db_url.startswith("mongodb"):
            self.db = MongoRepository(db_url, schema)
        elif db_url.startswith("postgresql"):
            self.db = PostgresRepository(db_url, schema)
        else:
            raise NotImplementedError("Database url not supported")

    # TODO - methods that we can add based on schema
