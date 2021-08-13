"""
Each app should be defined in the AppBuilder class

You can add new default routes by creating a new module in this package.
See `tenant_registration_route.py` for an example

Make sure to decorate each route with `failsafe` decorator that way app will not crash
and will log the error in app.log


"""


from .app_builder import AppBuilder