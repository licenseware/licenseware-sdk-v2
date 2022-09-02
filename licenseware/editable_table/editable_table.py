"""

EditableTable provided in this package is used to generate table metadata from a marshmallow Schema


From the schema provided `EditableTable(schema).specs` will return a list of editable tables metadata similar to this:

```js
[
  {
    "component_id": "ifmp_devicetables",
    "url": "http://localhost:5000/ifmp/devicetable",
    "path": "/devicetable",
    "order": 1,
    "style_attributes": {
      "width": "full"
    },
    "title": "All devicetables",
    "type": "editable_table",
    "columns": [
      {
        "name": "Id",
        "prop": "_id",
        "editable": false,
        "type": "string",
        "values": null,
        "required": false,
        "visible": false,
        "entities_url": "http://localhost:5000/ifmp/devicetable?_id=%7Bentity_id%7D",
        "entities_path": "/devicetable?_id=%7Bentity_id%7D"
      },
      {
        "name": "Is Parent To",
        "prop": "is_parent_to",
        "editable": true,
        "type": "entity",
        "values": null,
        "required": false,
        "visible": false,
        "entities_url": "http://localhost:5000/ifmp/devicetable?distinct_key=name&foreign_key=name&_id=%7Bentity_id%7D",
        "entities_path": "/devicetable?distinct_key=name&foreign_key=name&_id=%7Bentity_id%7D"
      },
      {
        "name": "Device Type",
        "prop": "device_type",
        "editable": false,
        "type": "enum",
        "values": [
          "Cluster",
          "Domain",
          "Physical",
          "Pool",
          "Unknown",
          "Virtual"
        ],
        "required": true,
        "visible": false,
        "entities_url": "http://localhost:5000/ifmp/devicetable?_id=%7Bentity_id%7D",
        "entities_path": "/devicetable?_id=%7Bentity_id%7D"
      },
    ]
  }
]

```

From the information provided up the front-end will know how to render each column based on: datatype(type), editable, required, visible parameters.


# TODO add pagination

By making a get request to the root url (`"url": "http://localhost:5000/ifmp/devicetable"`) all data will be returned from mongo. 


A get request with the `_id` query parameter will return the coresponding document from mongo.
`"entities_url": "http://localhost:5000/ifmp/devicetable?_id=%7Bentity_id%7D"` (`%7D` it's `}` with urlencode)


A post/put/delete request to root url with the modified/new document will modifiy the document.
   
**NOTE** 
The query params and payload will be merged and used as a mongo query! 
Any data manipulation operation can be done from the front-end.   


# TODO explore security risks



Bellow we have an example of using a schema to generate an editable table metadata and it's coresponding api.


We provide the information required for generating editable metadata in the `metadata` parameter.
Column names will be created from field names and other information's such as datatype, values(in case of `enum` datatype) etc will be taken from marshmallow `fields` specifications.


For metadata you can use either a dict or `metaspecs` function which has autocomplete.


```py

from marshmallow import Schema, fields, validate

from licenseware.common.constants import envs
from licenseware.editable_table import EditableTable, metaspecs
from licenseware.schema_namespace import MongoCrud, SchemaNamespace

from app.common.infrastructure_service import InfraService




class DeviceTableSchema(Schema):

    ''' IFMP devices editable table ''' # this will be the api doc
    
    class Meta:
    
        compound_indexes = [
            ['tenant_id', 'name'],
            ['tenant_id', 'name', 'device_type']
        ]
        simple_indexes = ['_id', 'tenant_id', 'name',
                   'is_parent_to', 'is_child_to',
                   'is_part_of_cluster_with', 'is_dr_with',
                   'device_type', 'virtualization_type',
                   'cpu_model'
                   ]


    _id = fields.Str(required=False, unique=True)
    tenant_id = fields.Str(required=True)
    
    name = fields.Str(required=True, unique=False, metadata=metaspecs(editable=True))

    is_parent_to = fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata={'editable': True, 'distinct_key': 'name', 'foreign_key': 'name'}
    )

    is_child_to = fields.Str(
        required=False, allow_none=True,
        metadata=metaspecs(editable=True, distinct_key='name', foreign_key='name') 
    )

    is_part_of_cluster_with =  fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata={'editable': True, 'distinct_key': 'name', 'foreign_key': 'name'}
    )
    is_dr_with =  fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata={'editable': True, 'distinct_key': 'name', 'foreign_key': 'name'}
    )

    capped = fields.Boolean(required=True, allow_none=False, metadata={'editable': True})
    total_number_of_processors = fields.Integer(required=False, allow_none=True, metadata={'editable': True})

    manufacturer = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    model = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    updated_at = fields.Str(required=False)
    raw_data = fields.Str(required=False, allow_none=True)

    source = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    source_system_id = fields.Str(required=False, allow_none=True, metadata={'editable': True})





# here we are inheriting from `MongoCrud` class which has default crud methods
# we are overwriting the `put_data` method
class DeviceOp(MongoCrud):
    
    def __init__(self, schema: Schema, collection: str):
        self.schema = schema
        self.collection = collection
        super().__init__(schema, collection)
    
    
    def put_data(self, flask_request):
        
        query = self.get_query(flask_request)
        
        return InfraService(
            schema=self.schema, 
            collection=self.collection
        ).replace_one(json_data=query)
        
    
# Here we are creating a restx namespace using the schema
DeviceNs = SchemaNamespace(
    schema=DeviceTableSchema,
    collection=envs.MONGO_COLLECTION_DATA_NAME, #default can be skipped
    methods=['GET', 'PUT', 'DELETE'], #default is ['GET', 'PUT', 'POST', 'DELETE'] 
    mongo_crud_class = DeviceOp # here we provide the modified crud operations class
).initialize()


# In the case of a crud operation overwrite we need to provide to `EditableTable` the restx namespace created up 
devices_table = EditableTable(
    title="All Devices",
    schema=DeviceTableSchema,
    namespace=DeviceNs # needed in case of an overwrite
)
 

# If no overwrites are necessary providing just the schema will be suficient 
devices_table = EditableTable(
    title="All Devices",
    schema=DeviceTableSchema
)
 
 
```

Later, in the base `__init__.py` file import the `EditableTable` instance and register it to the main `App`.


```py
from licenseware.common.constants import flags
from licenseware.app_builder import AppBuilder


from app.controllers.device_editable_controller import devices_table



App = AppBuilder(
    name = 'Infrastructure Mapper',
    description = 'IFMP (Infrastructure Mapper) is the ideal tool to help you get a complete picture of your entire infrastructure topology with comprehensive CPU, virtualization, and relationship details. You can combine IFMP data with data from other apps like ODBM (Oracle Database Manager) to generate consolidated reports showing your actual license utilization across your infrastructure.',
    flags = [flags.BETA]
)


App.register_editable_table(devices_table)

```

"""

import itertools
import re
from typing import List
from urllib.parse import urlencode

import marshmallow
from flask_restx import Namespace
from marshmallow import Schema

from licenseware.common.constants import envs


class EditableTable:
    def __init__(
        self,
        schema: type,
        title: str = None,
        namespace: Namespace = None,
        component_id: str = None,
        url: str = None,
        table_type: str = "editable_table",
        order: int = 1,
        style_attributes: dict = {"width": "full"},
    ):
        self.schema = schema
        self.namespace = namespace

        if "Table" not in self.schema.__name__:
            raise ValueError(
                "Schema provided to editable tables must contain in it's name 'Table' keyword (ex: DeviceTableSchema)"
            )

        self.schema_name = self.schema.__name__.replace("Schema", "").lower()
        self.names = self.schema_name
        self.component_id = component_id or self.component_id_from_schema()
        self.title = title or self.title_from_schema()
        self.path = url or self.url_from_schema()
        self.url = envs.BASE_URL + self.path
        self.table_type = table_type
        self.order = order
        self.style_attributes = style_attributes
        self.schema_dict = self.make_schema_dict()
        self.add_title_on_schema_meta()

    def add_title_on_schema_meta(self):
        """Adding title on Meta if not present or getting title if exists"""
        if hasattr(self.schema, "Meta"):
            if hasattr(self.schema.Meta, "title"):
                self.title = self.schema.Meta.title
            else:
                self.schema = type(
                    self.schema.__name__,
                    (self.schema,),
                    {"Meta": type("Meta", (self.schema.Meta,), {"title": self.title})},
                )
        else:
            self.schema = type(
                self.schema.__name__,
                (self.schema,),
                {"Meta": type("Meta", (), {"title": self.title})},
            )

    def url_from_schema(self):
        return f"/{self.schema_name}"

    def title_from_schema(self):
        return self.names

    def component_id_from_schema(self):
        return envs.APP_ID + "_" + self.names

    def make_schema_dict(self):

        field_dict = lambda data: {
            k: v
            for k, v in data.__dict__.items()
            if k not in ["default", "_creation_index", "missing", "inner"]
        }

        schema_dict = lambda declared_fields: {
            field: field_dict(data) for field, data in declared_fields.items()
        }

        return schema_dict(self.schema._declared_fields)

    @property
    def specs(self):
        return self.get_specifications()

    def get_specifications(self):
        return {
            "component_id": self.component_id,
            "url": self.url,
            "path": self.path,
            "order": self.order,
            "style_attributes": self.style_attributes,
            "title": self.title,
            "type": self.table_type,
            "columns": self.columns_spec_list(),
        }

    def columns_spec_list(self):

        columns_list = []
        for field_name, field_data in self.schema_dict.items():
            columns_list.append(
                {
                    "name": self.col_name(field_name),
                    "prop": self.col_prop(field_name),
                    "editable": self.col_editable(field_data),
                    "type": self.col_type(field_data),
                    "values": self.col_enum_values(field_data),
                    "required": self.col_required(field_data),
                    "visible": self.col_visible(field_name, field_data),
                    "hashable": self.col_hashable(field_name, field_data),
                    "entities_url": self.col_entities_url(field_data),
                }
            )

        return columns_list

    def col_entities_url(self, field_data, _get_only_path=False):
        """
        _id - device(doc) id which contains foreign_keys to get the distinct_keys
        foreign_key  - field name that contains ids to distinct_key
        metadata={'editable': False, 'distinct_key': 'name', 'foreign_key': 'is_parent_to'}
        """

        metadata = self.field_metadata(field_data)

        if "foreign_key" in metadata and metadata["foreign_key"] != None:
            params = urlencode(
                {"foreign_key": metadata["foreign_key"], "_id": "{entity_id}"}
            )

            return f"{self.path}?{params}" if _get_only_path else f"{self.url}?{params}"
        return None

    def col_entities_path(self, field_data):
        return self.col_entities_url(field_data, _get_only_path=True)

    def col_required(self, field_data):
        return field_data["required"]

    def col_visible(self, field_name, field_data):
        metadata = self.field_metadata(field_data)
        if "visible" in metadata:
            return metadata["visible"]
        if field_name.startswith("_"):
            return False
        if field_name in ["tenant_id"]:
            return False
        return False

    def col_hashable(self, field_name, field_data):
        metadata = self.field_metadata(field_data)
        if "hashable" in metadata:
            return metadata["hashable"]
        if field_name.startswith("_"):
            return False
        if field_name in ["tenant_id"]:
            return False
        return False

    def col_enum_values(self, field_data):

        try:

            if field_data["validate"] is None:
                return

            if isinstance(field_data["validate"], marshmallow.validate.OneOf):
                return field_data["validate"].choices

            if isinstance(field_data["validate"], list):
                return sorted(
                    list(
                        set(
                            itertools.chain(
                                *[data.choices for data in field_data["validate"]]
                            )
                        )
                    )
                )

        except Exception:
            # log.error(err)
            return None

    def col_name(self, field_name):
        return " ".join([f.capitalize() for f in field_name.split("_") if f != ""])

    def col_prop(self, field_name):
        return field_name

    def col_editable(self, field_data):
        metadata = self.field_metadata(field_data)
        if "editable" in metadata:
            return metadata["editable"]
        return False

    def col_type(self, field_data):

        metadata = self.field_metadata(field_data)

        if "type" in metadata:
            return metadata["type"]
        if "distinct_key" in metadata:
            return "entity"

        try:

            if isinstance(field_data["validate"], marshmallow.validate.OneOf):
                if len(field_data["validate"].choices) > 0:
                    return "enum"

            if isinstance(field_data["validate"], list):
                for data in field_data["validate"]:
                    if len(data["validate"].choices) > 0:
                        return "enum"

        except:
            ...

        try:
            invalid_message = field_data["error_messages"]["invalid"]
            return re.search(r"Not a valid (.*?)\.", invalid_message).group(1).lower()
        except:
            ...

    def field_metadata(self, field_data):
        if "metadata" in field_data:
            return field_data["metadata"]
        return ""


def editable_tables_from_schemas(schemas_list: List[Schema]) -> List[dict]:
    editable_tables = []
    for schema in schemas_list:
        table = EditableTable(schema)
        editable_tables.append(table.specs)
    return editable_tables
