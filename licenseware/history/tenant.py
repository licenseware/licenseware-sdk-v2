import inspect


def get_tenant_id_from_args(func_args):
    for arg in func_args:
        if hasattr(arg, 'headers'):  # flask request
            try:
                return func_args[0].headers.get("TenantId")
            except:
                pass
    return None


def get_tenant_id_from_kwargs(func_kwargs):
    if 'tenant_id' in func_kwargs:
        return func_kwargs['tenant_id']
    elif 'flask_request' in func_kwargs:
        return func_kwargs['flask_request'].headers.get("TenantId")
    return None


def get_tenant_id_from_defaults(func):
    return inspect.signature(func).parameters['tenant_id'].default


def get_tenant_id(func, func_args, func_kwargs):

    tenant_id = get_tenant_id_from_args(func_args)

    if tenant_id is None:
        tenant_id = get_tenant_id_from_kwargs(func_kwargs)
    if tenant_id is None:
        tenant_id = get_tenant_id_from_defaults(func)

    return tenant_id
