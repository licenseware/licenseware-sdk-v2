"""

In the `app_builder` package we define the `app` and build the api.   

Make sure to decorate each route with `failsafe` decorator that way app will not crash
and will log the error in app.log

There are 2 ways we can add new endpoints to the main Api:

- The first one is to pass instantiated `api` object from `app_builder` to a function, use that `api` object then pass it back to `AppBuilder` class. See `app_activation_route` for a full example;

- The second one is to create a new package (folder) just like we did with `uploads_namespace`, declare the `Namespace` in the __init__.py file and the functions needed. The functions and the namespace created will be imported in the `AppBuilder` class and invoked. See `uploads_namespace` for a full example.


All default routes should be created in this package 


"""


from .app_builder import AppBuilder
