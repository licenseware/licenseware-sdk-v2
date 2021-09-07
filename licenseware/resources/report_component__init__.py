from .{{ component_id }} import {{ component_id.replace('_', '').capitalize() }}




{{ component_id }}_component = {{ component_id.replace('_', '').capitalize() }}(
    title="{{ component_id.replace('_', ' ').capitalize() }}",
    component_id="{{ component_id }}",
    component_type="{{ component_type }}"
)


