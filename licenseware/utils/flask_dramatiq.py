"""

This is just a refactor of flask-dramatiq https://flask-dramatiq.readthedocs.io/en/latest/

Customized to be used with Redis database.


Usage:

```py

from licenseware.utils.flask_dramatiq import Dramatiq

broker = Dramatiq(
    url = os.getenv('REDIS_CONNECTION_STRING')
)

```

You can use `broker` object to decorate function workers
The broker instantiation is already done by the licenseware sdk

You can use it like bellow

```py

from licenseware.utils.dramatiq_redis_broker import broker


@broker.actor()
def worker_func(event):
    return "some data"
    
```

The broker is used in `UploaderBuilder` to decorate `worker_functions`.
The `AppBuilder` class will wrap the worker with the flask app context.

Background worker can be started using the default dramatiq CLI or via sdk

```bash

dramatiq main:App.broker -p4 --watch ./ --queues odb

```

Using the licenseware CLI if DEBUG is found true in evironment variables it will start with the `--watch` flag.

```bash

licenseware start-background-worker

```



"""

from flask import Flask
from dramatiq import set_broker
from threading import local
from dramatiq import Middleware
from dramatiq import actor as register_actor
from dramatiq.middleware import default_middleware
from dramatiq.brokers.redis import RedisBroker



# PREPS

class AppContextMiddleware(Middleware):
    # Setup Flask app for actor. Borrowed from
    # https://github.com/Bogdanp/flask_dramatiq_example.

    state = local()

    def __init__(self, app):
        self.app = app

    def before_process_message(self, broker, message):
        context = self.app.app_context()
        context.push()

        self.state.context = context

    def after_process_message(
            self, broker, message, *, result=None, exception=None):
        try:
            context = self.state.context
            context.pop(exception)
            del self.state.context
        except AttributeError:
            pass

    after_skip_message = after_process_message



class LazyActor(object):
    # Intermediate object that register actor on broker an call.

    def __init__(self, extension, fn, kw):
        self.extension = extension
        self.fn = fn
        self.kw = kw
        self.actor = None

    def __call__(self, *a, **kw):
        return self.fn(*a, **kw)

    def __repr__(self):
        return '<%s %s.%s>' % (
            self.__class__.__name__,
            self.fn.__module__, self.fn.__name__,
        )

    def __getattr__(self, name):
        if not self.actor:
            raise AttributeError(name)
        return getattr(self.actor, name)

    def register(self, broker):
        self.actor = register_actor(broker=broker, **self.kw)(self.fn)

    # Next is regular actor API.

    def send(self, *a, **kw):
        return self.actor.send(*a, **kw)

    def send_with_options(self, *a, **kw):
        return self.actor.send_with_options(*a, **kw)


# BROKER    

class Dramatiq:
    
    def __init__(self, *,  app:Flask = None, url:str = None, middleware: any = None):
        
        self.app = None
        self.url = url
        self.actors = []
        
        if middleware is None: middleware = [m() for m in default_middleware]
        self.middleware = middleware

        if app: self.init_app(app)
        
        
    def add_app_to_self(self, app: Flask):
        if self.app is not None: 
            raise Exception("Flask 'app' can be provided only on 'init_app' or 'Dramatiq' class instantiation")
        self.app = app
        
        
    def init_app(self, app:Flask):
        self.add_app_to_self(app)
        
        middleware = [AppContextMiddleware(self.app)] + self.middleware
        
        if self.url.startswith('redis'):
            self.broker = RedisBroker(url=self.url, middleware=middleware)
        else: raise Exception("Only 'Redis' broker is supported")
            
        for actor in self.actors:
            actor.register(broker=self.broker)
            
        set_broker(self.broker)
    
        return self.broker
 
    
    def actor(self, fn=None, **kw):
        
        def decorator(fn):
            lazy_actor = LazyActor(self, fn, kw)
            self.actors.append(lazy_actor)
            if self.app:
                lazy_actor.register(self.broker)
            return lazy_actor

        if fn: return decorator(fn)
        return decorator
