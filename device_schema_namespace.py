from marshmallow import Schema, fields, validate


class DeviceCRUDSchema(Schema):
    
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
        

    tenant_id = fields.Str(required=True, metadata={'editable': False, 'visible': False})
    _id = fields.Str(required=False, unique=True, metadata={'editable': False})
    name = fields.Str(required=True, unique=False, metadata={'editable': True})

    is_parent_to = fields.List(
        fields.Str(), required=False, allow_none=True,
        metadata={'editable': True, 'distinct_key': 'name', 'foreign_key': 'name'}
    )

    is_child_to = fields.Str(
        required=False, allow_none=True,
        metadata={'editable': True, 'distinct_key': 'name', 'foreign_key': 'name'}
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
    device_type = fields.Str(required=True, validate=[
        validate.OneOf([
            "Virtual", "Pool", "Domain", "Physical", "Cluster", "Unknown"
        ], error='Only allowed values are "Virtual", "Pool", "Physical", "Cluster", "Unknown"')
    ], metadata={})
    virtualization_type = fields.Str(required=True, validate=[
        validate.OneOf([
            "Solaris", "VMWare", "OracleVM", "AIX", "HP-UX", "Hyper-V", "Physical", "Other"
        ],
            error='Only allowed values are "Solaris", "VMWare", "OracleVM", "AIX", "HP-UX", "Hyper-V", "Physical", "Other"')
    ], metadata={})

    operating_system_type = fields.Str(required=False, allow_none=True, validate=[
        validate.OneOf([
            "Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"
        ], error='Only allowed values are "Solaris", "ESX", "Linux", "AIX", "HP-UX", "Windows", "Other"')
    ], metadata={})
    operating_system_caption = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    cpu_model = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    total_number_of_processors = fields.Integer(required=False, allow_none=True, metadata={'editable': True})
    total_number_of_cores = fields.Integer(required=False, allow_none=True, metadata={'editable': True})
    total_number_of_threads = fields.Integer(required=False, allow_none=True, metadata={'editable': True})
    oracle_core_factor = fields.Float(required=False, allow_none=True, metadata={'editable': True})

    manufacturer = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    model = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    updated_at = fields.Str(required=False)
    raw_data = fields.Str(required=False, allow_none=True)

    source = fields.Str(required=False, allow_none=True, metadata={'editable': True})
    source_system_id = fields.Str(required=False, allow_none=True, metadata={'editable': True})
