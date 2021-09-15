from .{{ component_id }} import {{ component_id.split('_') | map('title') | join('') }}




{{ component_id }}_component = {{ component_id.split('_') | map('title') | join('') }}(
    title="{{ component_id.split('_') | map('title') | join(' ') }}",
    component_id="{{ component_id }}",
    component_type="{{ component_type }}"
)


