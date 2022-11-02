from . import history


class HistoryLogger(type):
    def __new__(cls, name, bases, namespace, **kwds):
        namespace = {
            k: v if k.startswith("__") else history.log(v) for k, v in namespace.items()
        }
        decorated_class_methods = type.__new__(cls, name, bases, namespace)
        assert hasattr(
            decorated_class_methods, "run_processing_pipeline"
        ), "Please provide `run_processing_pipeline` method which will trigger the processing for each filepath"
        return decorated_class_methods
