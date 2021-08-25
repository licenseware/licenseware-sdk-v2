"""

In the `app_builder` package we define the `app` and build routes.   

Make sure to decorate each route with `failsafe` decorator that way app will not crash
and will log the error in app.log


"""


from .app_builder import AppBuilder