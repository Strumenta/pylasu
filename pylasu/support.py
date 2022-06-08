def extension_method(cls):
    """Installs the decorated function as an extension method on cls.
    See https://mail.python.org/pipermail/python-dev/2008-January/076194.html"""
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator
