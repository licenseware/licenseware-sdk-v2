from celery import Celery



class CeleryBroker:

    def __init__(self, 
        host:str = None, 
        port:int = None, 
        db:int = 0,
        password:str = None
    ) -> None:

        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.celery = Celery( 
            broker=f'redis://:{self.password}@{self.host}:{self.port}/{self.db}' if self.password else f'redis://{self.host}:{self.port}/{self.db}' 
        )
        # self.celery.autodiscover_tasks()
        
    
    def actor(self, fn, **kw):

        def decorator(fn):

            class DramatiqCeleryAdapter:
                def __init__(self, broker, func) -> None:
                    self.task = broker.celery.task(func, **kw)

                def send(self, *args, **kwargs):
                    return self.task.delay(*args, **kwargs)

            return DramatiqCeleryAdapter(self, fn)

        return decorator(fn)


        
