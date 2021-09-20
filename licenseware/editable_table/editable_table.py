import os, re, itertools
from flask_restx.namespace import Namespace
from marshmallow import Schema
from licenseware.common.constants import envs
from urllib.parse import urlencode
from typing import List

from licenseware.utils.logger import log


class EditableTable:

    def __init__(
        self, 
        schema: Schema, 
        namespace: Namespace = None,
        component_id: str = None, 
        title: str = None,
        url: str = None, 
        table_type: str = "editable_table",
        order: int = 1,
        style_attributes: dict = {'width': 'full'}
    ):
        self.schema = schema
        self.namespace = namespace
        
        if not "Table" in self.schema.__name__:
            raise ValueError("Schema provided to editable tables must contain in it's name 'Table' keyword (ex: DeviceTableSchema)")
        
        self.schema_name = self.schema.__name__.replace('Schema', '').lower()
        self.names = self.schema_name
        if not self.names.endswith('s'):
            self.names = self.names + 's' #plural
    
        self.component_id = component_id or self.component_id_from_schema()
        self.title = title or self.title_from_schema()
        self.path = (url or self.url_from_schema())
        self.url = envs.BASE_URL + self.path
        self.table_type = table_type
        self.order = order
        self.style_attributes = style_attributes
        self.schema_dict = self.make_schema_dict()
        
        
    def url_from_schema(self):
        return f'/{self.schema_name}'

    def title_from_schema(self):
        return 'All ' + self.names

    def component_id_from_schema(self):
        return envs.APP_ID + "_" + self.names

    def make_schema_dict(self):

        field_dict = lambda data: {
            k:v for k, v in data.__dict__.items() 
            if k not in ['default', '_creation_index', 'missing', 'inner']
        }

        schema_dict = lambda declared_fields: {
            field: field_dict(data)
            for field, data in declared_fields.items()
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
            "columns": self.columns_spec_list()
        }

    def columns_spec_list(self):

        columns_list = []
        for field_name, field_data in self.schema_dict.items():
            columns_list.append({
                "name": self.col_name(field_name),
                "prop": self.col_prop(field_name),
                "editable": self.col_editable(field_data),
                "type": self.col_type(field_data),
                "values": self.col_enum_values(field_data),
                "required": self.col_required(field_data),
                "visible": self.col_visible(field_name, field_data),
                "entities_url": self.col_entities_url(field_data),
                "entities_path": self.col_entities_path(field_data),
            })

        return columns_list


    def col_entities_url(self, field_data, _get_only_path=False):
        """
            _id - device(doc) id which contains foreign_keys to get the distinct_keys
            distinct_key - mongo's unique_key
            foreign_key  - field name that contains ids to distinct_key
            metadata={'editable': False, 'distinct_key': 'name', 'foreign_key': 'is_parent_to'}
        """

        metadata = self.field_metadata(field_data)

        if 'distinct_key' and 'foreign_key' in metadata: 
            params = urlencode({
                'distinct_key': metadata['distinct_key'], 
                'foreign_key' : metadata['foreign_key'],
                '_id': '{entity_id}'
            })
            
            return f"{self.path}?{params}" if _get_only_path else f"{self.url}?{params}"

        # Create query params with just _id
        params = urlencode({'_id': '{entity_id}'})
        
        return f"{self.path}?{params}" if _get_only_path else f"{self.url}?{params}"
    
    
    def col_entities_path(self, field_data):
        return self.col_entities_url(field_data, _get_only_path=True)
        

    def col_required(self, field_data):
        return field_data['required']

    def col_visible(self, field_name, field_data):
        metadata = self.field_metadata(field_data)
        if 'visible' in metadata: return metadata['visible']
        if field_name.startswith('_'): return False
        if field_name in ['tenant_id', '_id']: return False
        return False

    def col_enum_values(self, field_data):
        try:
            choices_list = []
            for data in field_data['validate']:
                choices_list.append(data.__dict__['choices'])

            choices_list = sorted(list(set(itertools.chain(*choices_list))))
            return choices_list
        except: 
            return None
                  
    def col_name(self, field_name):
        return " ".join([f.capitalize() for f in field_name.split('_') if f != ""])

    def col_prop(self, field_name):
        return field_name

    def col_editable(self, field_data):
        metadata = self.field_metadata(field_data)
        if 'editable' in metadata: return metadata['editable']
        return False

    def col_type(self, field_data):
        
        metadata = self.field_metadata(field_data)

        if 'type' in metadata: return metadata['type']
        if 'distinct_key' in metadata: return 'entity'

        try:
            if field_data['validate'][0].__dict__['choices']:
                return 'enum'
        except: ...

        try:
            invalid_message = field_data['error_messages']['invalid']
            return re.search(r'Not a valid (.*?)\.', invalid_message).group(1).lower()
        except:...
        
    
    def field_metadata(self, field_data):
        if 'metadata' in field_data:
            return field_data['metadata']
        return ""


def editable_tables_from_schemas(schemas_list: List[Schema]) -> List[dict]:
    editable_tables = []
    for schema in schemas_list:
        table = EditableTable(schema)
        editable_tables.append(table.specs)
    return editable_tables
