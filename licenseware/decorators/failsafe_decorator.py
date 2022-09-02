import traceback
from functools import wraps

from licenseware.utils.logger import log


def failsafe(
    *dargs, fail_code=0, success_code=0, error_msg="Failed processing your request!"
):
    """
    Prevents a function to raise an exception and break the app.
    Returns a string with the exception and saves the traceback in app.log
    If fail_code or success_code is specified then a json response will be returned.

    @failsafe
    def fun1(): raise Exception("test")
    print(fun1())
    >>test

    @failsafe(fail_code=500)
    def fun2(): raise Exception("test")
    print(fun2())
    >> ({'status': 'fail', 'message': 'test'}, 500)

    @failsafe(fail_code=500, success_code=200)
    def fun3(): return "test"
    print(fun3())
    >> ({'status': 'success', 'message': 'test'}, 200)

    This decorator is very useful to prevent app crashes but still logging them

    Ex:

    @api.route('/)
    @failsafe(fail_code=500)
    def viewfunc():
        raise Exception("Inevitable app crash")

    When called the route up will return:
    {'status': 'fail', 'message': "Inevitable app crash"}, 500

    Unknown/Unhandled errors maybe not so useful for the user.

    But with the errors you raised there is no issue.

    """

    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                if success_code:
                    return {"status": "success", "message": response}, success_code
                return response
            except Exception as err:
                log.error(str(err))
                log.error(traceback.format_exc())
                if fail_code:
                    return {"status": "fail", "message": error_msg}, fail_code
                return error_msg

        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
