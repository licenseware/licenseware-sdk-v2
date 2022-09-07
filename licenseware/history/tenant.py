from licenseware.history.func import get_value_from_func


def get_tenant_id(func, func_args, func_kwargs):
    return get_value_from_func(func, func_args, func_kwargs, "tenant_id", "TenantId")
