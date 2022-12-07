def getannotations(cls):
    import inspect
    try:  # On Python 3.10+
        return inspect.getannotations(cls)
    except AttributeError:
        if isinstance(cls, type):
            return cls.__dict__.get('__annotations__', None)
        else:
            return getattr(cls, '__annotations__', None)
