def passthrough_methods(methods, attr):
    def decorate(cls):
        def to_attr(arg):
            if isinstance(arg, cls):
                return getattr(arg, attr)
            return arg
        def implement_forwarding(method):
            @functools.wraps(method)
            def callback(self, *args, **kwargs):
                return getattr(getattr(self, attr), method)(*map(to_attr, args), **kwargs)
            return callback
        for method in methods:
            setattr(cls, method, implement_forwarding(method))
        return cls
    return decorate

"""
eg:

@passthrough_methods([
    "__eq__",
    "__ne__",
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
    "__bool__",
    "__add__",
    "__radd__",
    "__mul__",
    "__rmul__",
    "__sub__",
    "__div__",
], "_value")
class Box:
  def __init__(self, value):
    self._value = value
"""
