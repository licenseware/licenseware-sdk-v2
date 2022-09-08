"""

Usage:

```py

from marshmallow import Schema, fields
from licenseware.repository.postgres import PostgresRepository

db_url = f"postgresql://{ os.environ['POSTGRES_USERNAME'] }:{ os.environ['POSTGRES_PASSWORD'] }@{ os.environ['POSTGRES_HOSTNAME'] }/{ os.environ['POSTGRES_DB'] }"

db = PostgresRepository(db_url)


# Define a marshmallow schema

class UsersSchema(Schema):
    
    class Meta:
        __tablename__ = 'users'
    
    name = fields.String(required=True)
    email = fields.String(required=True)
    address = fields.String(required=True)


# __tablename__ is optional, if not completed `users` will be the table name from schema.__name__

db.register_schema(UsersSchema)


# Insert some data

db.insert_one(
    schema = UsersSchema,
    name = 'Travis',
    email = 'travis@gmail.com',
    address = 'Oradea, Centru'
)


# Insert some data in bulk

db.insert_many(
    schema = UsersSchema,
    data=[
        {
            'name': 'Anakin',
            'email': 'anakin@gmail.com',
            'address': 'Calea Lactee'
        },
        {
            'name': 'Bum',
            'email': 'bum@gmail.com',
            'address': 'Calea Lactee'
        },
        {
            'name': 'Doka',
            'email': 'doka@gmail.com',
            'address': 'Calea Lactee'
        }
    ]
)


# Fetching some data 

# First item that matched
db.fetch_one(schema_name="UsersSchema", email='travis@gmail.com')
db.fetch_by_id(schema_name="UsersSchema", id=13)

# All items that matched query
db.fetch_many(schema_name="UsersSchema", address='Oradea, Centru')

# All table
db.fetch_many(schema_name="UsersSchema")



# SQLAlchemy models can be created by inheriting from declarative base (db.Base)

class UsersTable(db.Base):
    
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True} 
    
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    address = sa.Column(sa.String)


# Insert with tuple of sqlalchemy model and marshmallow schema for validation

db.insert_one(
    schema = (UsersTable, UsersSchema),
    name = 'John',
    email = 'john@gmail.com',
    address = 'Iasi, Centru'
)

# Count items matched by query

count_nbr = db.count(schema_name='UsersSchema', address='Calea Lactee')


# Update some data

db.update_one(
    schema_name='UsersSchema',
    filters={'name':'Birt'},
    data={
        'email': 'birt_updated@gmail.com'
    }
)


db.update_on_id(
    schema_name='UsersSchema', 
    id=user['id'], 
    data={'email': 'birt@gmail.com'}
)



db.update_many(
    schema_name='UsersSchema',
    filters={'address': 'Calea Lactee'},
    data={
        'address': 'Mars, Calea Lactee'
    }
)


# Delete some data


db.delete_one(
    schema_name='UsersSchema',
    email='birt@gmail.com'
)


db.delete_by_id(
    schema_name='UsersSchema',
    id=user['id']
)

db.delete_many(schema_name='UsersSchema')



# Connecting to bare bones sqlalchemy 


with db.engine.connect() as conn:
    
    result = conn.execute(sa.insert(UsersTable),
            [
                {
                    'name': 'Etra',
                    'email': 'etra@gmail.com',
                    'address': 'Budabesta'
                },
                {
                    'name': 'Tyron',
                    'email': 'tyron@gmail.com',
                    'address': 'Budabesta'
                },
                {
                    'name': 'Pesta',
                    'email': 'pesta@gmail.com',
                    'address': 'Budabesta'
                }
            ]
        )
    

# or using the session object with raw sql or sqlalchemy's sql builder


sql_query = "SELECT * FROM users"

cursor = db.execute(sql_query)

# print(cursor.all())

users = db.deserialize(schema_name='UsersSchema', cursor_data=cursor.all())

# print(users)


# the sql query can be just a string

sql_query = "DELETE FROM users *"

cursor = db.execute(sql_query)


# You set commit to true on execute or you can commit later

db.session.commit()




```

All migrations will be handled automatically


# TODO integrate column paramters in marshmallow schema
# TODO include Base.metadata in PostgresMigrations



"""

from collections.abc import Iterable
from typing import List, Union

import sqlalchemy as sa
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

from licenseware.repository.interface import RepositoryInterface
from licenseware.repository.postgres.postgres_migrations import PostgresMigrations

# Marshmallow to Sqlalchemy fields mapper
# Only strings, integers, floats and booleans are suported for now
MATOSA_MAPPER = {
    fields.String: sa.String,
    fields.Str: sa.String,
    fields.Integer: sa.Integer,
    fields.Int: sa.Integer,
    fields.Float: sa.Float,
    fields.Boolean: sa.Boolean,
    fields.Bool: sa.Boolean,
}


class PostgresRepository(RepositoryInterface):
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.engine = sa.create_engine(db_url)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Base = declarative_base(bind=self.engine)
        self.registered_tables = {}
        self.registered_schemas = {}

    def create_all(self):
        """Create connection to db, create all tables and generate migration files"""

        self.Base.metadata.create_all()
        migrations = PostgresMigrations(self.db_url, target_metadata=self.Base.metadata)
        migrations.make_migrations()

    def register_schema(self, schema: Schema) -> str:
        """Register schema"""

        table = self._get_table_from_schema(schema)
        self.registered_tables[schema.__name__] = table
        self.registered_schemas[schema.__name__] = schema

        if not self.has_table(table.__tablename__):
            self.create_all()  # create table if doesn't exist

        return table.__tablename__

    # Fetching data

    def _deserialize_value(self, d: any, field_name: str, idx: int):

        if isinstance(d, list):
            for item in d:
                if isinstance(item, tuple):
                    return item[idx]

        if isinstance(d, Iterable):
            if len(d) == 1:
                return getattr(d[0], field_name)

        return getattr(d, field_name)

    def deserialize(self, schema_name: str, cursor_data: any):

        if cursor_data is None:
            return [{}]

        schema = self.registered_schemas[schema_name]

        datali = []
        for d in cursor_data:

            data_dict = {}

            # Getting the id
            data_dict["id"] = self._deserialize_value(d, field_name="id", idx=0)

            for idx, field_name in enumerate(schema().declared_fields.keys()):
                data_dict[field_name] = self._deserialize_value(d, field_name, idx + 1)

            datali.append(data_dict)

        return datali

    def fetch(
        self,
        schema_name: str,
        id: str = None,
        first: bool = False,
        limit: int = None,
        skip: int = None,
        **filters,
    ) -> List[dict]:
        """
        TODO limit and skip
        """

        first = first or ("id" in filters and len(filters) == 1)

        table = self.registered_tables[schema_name]
        filters_string = ", ".join(
            [f"table.{field} == filters['{field}']" for field in filters]
        )
        sql_query = (
            sa.select(table).where(eval(filters_string))
            if filters_string
            else sa.select(table)
        )

        cursor = self.execute(sql_query)

        cursor_data = cursor.first() if first else cursor.all()
        deserialized_data = self.deserialize(schema_name, cursor_data)

        return deserialized_data[0] if first else deserialized_data

    def fetch_one(self, schema_name: str, **filters) -> dict:
        """Get first item match"""
        return self.fetch(schema_name, first=True, **filters)

    def fetch_by_id(self, schema_name: str, id: str) -> dict:
        """Get first item match by id"""
        return self.fetch(schema_name, first=True, id=id)

    def fetch_many(self, schema_name: str, **filters) -> List[dict]:
        """Get all items that matched"""
        return self.fetch(schema_name, **filters)

        # Inserting new data

    def _sa_field(self, ma_field):
        try:
            return MATOSA_MAPPER[type(ma_field)]
        except:
            raise ValueError(
                "Only strings, integers, floats and booleans are suported for the moment"
            )

    def _get_table_name_from_schema(self, schema: Schema):

        if self.registered_tables.get(schema.__name__):
            raise Exception(f"Schema '{schema.__name__}' already registered")

        table_name = None
        if hasattr(schema, "Meta"):
            if hasattr(schema.Meta, "__tablename__"):
                table_name = schema.Meta.__tablename__

        if not table_name:
            table_name = schema.__name__.replace("Schema", "").lower()

        return table_name

    def _get_columns(self, schema: Schema):

        sa_cols = []
        for field_name, temp_field_type in schema().declared_fields.items():
            field_type = self._sa_field(temp_field_type)
            sa_cols.append(sa.Column(field_name, field_type))
        return sa_cols

    def _get_table_from_schema(self, schema: Schema):
        """Convert a marshmallow schema to a sqlalchemy model"""

        table_name = self._get_table_name_from_schema(schema)
        columns = self._get_columns(schema)

        Table = sa.Table(
            table_name,
            self.Base.metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            *columns,
            extend_existing=True,
        )

        Model = type(table_name, (object,), {"__tablename__": table_name})

        mapper(Model, Table)

        return Model

    def has_table(self, table_name: str):

        has_table = sa.inspect(self.engine).dialect.has_table(
            self.engine.connect(), table_name
        )

        return has_table

    def execute(self, sql_query: str, commit: bool = False) -> CursorResult:
        """
        Execute SQLAlchemy on db queries like:
        sql_query = select(UsersTable).where(UsersTable.name == 'John')

        Returns a cursor from which you can get results.

        """

        cursor: CursorResult = self.session.execute(
            sa.text(sql_query) if isinstance(sql_query, str) else sql_query
        )

        if commit:
            self.session.commit()

        return cursor

    def insert(self, schema: Schema, data: Union[dict, List[dict]]) -> CursorResult:
        """Insert dict or list of dict to db"""

        assert isinstance(data, dict) or isinstance(data, list)
        if isinstance(data, dict):
            data = [data]

        if isinstance(schema, tuple):
            table = schema[0]
            schema[1](many=True).load(data)  # marshmallow validate
        elif hasattr(schema, "__tablename__"):
            table = schema  # it's an SQLAlchemy Model
        else:
            schema(many=True).load(data)  # marshmallow validate
            table = self.registered_tables[schema.__name__]

        sql_query = sa.insert(table).values(data).returning(sa.text("id"))
        cursor = self.execute(sql_query, commit=True)

        return cursor.all()

    def insert_one(
        self, schema: Schema, data: dict = None, **data_kwargs
    ) -> CursorResult:
        """Insert dict to db"""
        return self.insert(schema, data or data_kwargs)

    def insert_with_id(
        self, schema: Schema, id: Union[str, int], data: dict = None, **data_kwargs
    ) -> CursorResult:
        """Insert dict with a specific 'id'"""
        raise NotImplementedError

    def insert_many(
        self, schema: Schema, data: List[dict], validate_percentage: float = 1.0
    ) -> CursorResult:
        """
        TODO `validate_percentage`: what percentage of the list of data provided should be validated (0.5 is 50%)
        """
        return self.insert(schema, data)

    # Updating existing data

    def count(self, schema_name: str, sql_query: any = None, **filters) -> int:

        table = self.registered_tables[schema_name]

        if not sql_query:
            filters_string = ", ".join(
                [f"table.{field} == filters['{field}']" for field in filters]
            )
            sql_query = (
                sa.select(table).where(eval(filters_string))
                if filters_string
                else sa.select(table)
            )

        cursor = self.execute(sql_query)
        counted_items = len(cursor.all())

        # TODO not working
        # counted_items = self.session.query(sa.select([sa.func.count()]).select_from(sql_query)).count()

        return counted_items

    def _validate_on_update(self, schema_name: str, data: Union[dict, List[dict]]):

        try:
            # marshmallow validate
            schema = self.registered_schemas[schema_name]

            schema(many=True).load(data) if isinstance(data, list) else schema().load(
                data
            )

        except ValidationError as Errors:

            # When updating we are only interested if the field to be updated is valid

            errors_dict = Errors.normalized_messages()

            if isinstance(data, list):
                for d in data:
                    field_found = set.intersection(
                        set(errors_dict.keys()), set(d.keys())
                    )
                    if field_found:
                        raise Errors
            else:
                field_found = set.intersection(
                    set(errors_dict.keys()), set(data.keys())
                )
                if field_found:
                    raise Errors

    def update(
        self,
        schema_name: str,
        filters: dict,
        data: Union[dict, List[dict]],
        first: bool = False,
    ) -> CursorResult:
        """ """

        self._validate_on_update(schema_name, data)

        table = self.registered_tables[schema_name]

        counted_items = self.count(schema_name, **filters)
        if first is True:
            if counted_items != 1:
                raise ValueError("Can't update one item with given filters")

        filters_string = ", ".join(
            [f"table.{field} == filters['{field}']" for field in filters]
        )
        sql_query = sa.update(table).where(eval(filters_string)).values(**data)

        cursor = self.execute(sql_query, commit=True)

        return cursor

    def update_one(self, schema_name: str, filters: dict, data: dict) -> CursorResult:
        """Update one item"""
        return self.update(schema_name, filters=filters, data=data, first=True)

    def update_on_id(
        self, schema_name: str, id: Union[str, int], data: dict
    ) -> CursorResult:
        """Update one item using the id"""
        return self.update(schema_name, filters={"id": id}, data=data, first=True)

    def update_many(
        self,
        schema_name: str,
        filters: dict,
        data: List[dict],
        validate_percentage: float = 1.0,
    ) -> CursorResult:
        """
        Update many
        TODO `validate_percentage`: what percentage of the list of data provided should be validated (0.5 is 50% of items in list)
        """
        return self.update(schema_name, filters=filters, data=data)

    # Deleting existing data

    def delete(
        self, schema_name: str, filters: dict, first: bool = False
    ) -> CursorResult:
        """Delete items"""

        table = self.registered_tables[schema_name]

        counted_items = self.count(schema_name, **filters)
        if first is True:
            if counted_items != 1:
                raise ValueError("Can't delete one item with given filters")

        filters_string = ", ".join(
            [f"table.{field} == filters['{field}']" for field in filters]
        )
        sql_query = (
            sa.delete(table).where(eval(filters_string))
            if filters_string
            else sa.delete(table)
        )

        cursor = self.execute(sql_query, commit=True)

        return cursor

    def delete_one(self, schema_name: str, **filters) -> CursorResult:
        """Delete one item"""
        return self.delete(schema_name, filters, first=True)

    def delete_by_id(self, schema_name: str, id: str) -> CursorResult:
        """Delete one item using the id provided"""
        return self.delete(schema_name, filters={"id": id}, first=True)

    def delete_many(self, schema_name: str, **filters) -> CursorResult:
        """Delete items that match filters"""
        return self.delete(schema_name, filters)
