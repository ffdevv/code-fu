from typing import Optional

def proxy_of_class(Class):
  class Proxy(Class):
    """
    A Proxy class that forwards all attribute accesses to the underlying instance.
    Access is prevented until the `init` method is called.
    """
    def __init__(self, *args, **kwargs):
      """
      Initializes the Proxy.

      Args:
        *args: Positional arguments to be passed to the parent class.
        **kwargs: Keyword arguments to be passed to the parent class.
      """
      self._proxied = None

    def __getattribute__(self, name):
      """
      Overrides attribute access for the instance.

      Raises a `RuntimeError` if the Proxy has not been initialized and the attribute
      being accessed is not `_proxied`, `init`, `replace`, `__repr__`, or `__class__`.

      Args:
        name (str): The name of the attribute being accessed.

      Returns:
        The value of the attribute.
      """
      pxd = super().__getattribute__("_proxied")
      if pxd is None:
        if not name in ["_proxied", "init", "replace", "__repr__", "__class__"]:
          raise RuntimeError("Proxy not yet initialized")
        return super().__getattribute__(name)
      return pxd.__getattribute__(name)

    def __setattr__(self, name, value):
      """
      Overrides attribute setting for the instance.

      Raises a `RuntimeError` if the Proxy has not been initialized and the attribute
      being accessed is not `_proxied` or `init`.

      Args:
        name (str): The name of the attribute being accessed.
        value (any): The value to set the attribute to.

      Returns:
        The value of the attribute.
      """
      if not name == "_proxied":
        pxd = super().__getattribute__("_proxied")
        if pxd is None:
          raise RuntimeError("Proxy not yet initialized")
        return pxd.__setattr__(name, value)
      return super().__setattr__(name, value)

    def init(self, *args, **kwargs):
      """
      Initializes the Proxy by initializing the underlying instance.

      Args:
        *args: Positional arguments to be passed to the parent class.
        **kwargs: Keyword arguments to be passed to the parent class.
      """
      self._proxied = Class(*args, **kwargs)

    def replace(self, instance: Class):
      """
      Replaces the proxied instance with the given instance.

      Args:
        instance (Class): The instance to replace the proxied instance with.
      """
      self._proxied = instance

    def __repr__(self):
      """
      Returns a string representation of the Proxy instance.

      Returns:
        A string representation of the Proxy instance.
      """
      cls = super().__getattribute__("__class__")
      return "ProxyOf" + cls.__bases__[0].__name__

  return Proxy
