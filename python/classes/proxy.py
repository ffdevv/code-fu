def proxy_of_class(Class):
    """
    Factory function that returns a Proxy class that inherits from the given class.

    The Proxy class intercepts attribute access to the instance of the given class,
    preventing access until the `init` method is called. Once initialized, the Proxy
    forwards all attribute accesses to the underlying instance.

    Args:
        Class: The class to proxy.

    Returns:
        A Proxy class that inherits from the given class.
    """
    class Proxy(Class):
        def __init__(self, *args, **kwargs):
            """
            Initializes the Proxy.

            Sets the `_inited` attribute to `False`, indicating that the Proxy has
            not yet been initialized.

            Args:
                *args: Positional arguments to be passed to the parent class.
                **kwargs: Keyword arguments to be passed to the parent class.
            """
            self._inited = False

        def __getattribute__(self, name):
            """
            Overrides the attribute access of the instance.

            If the attribute being accessed is not one of `_inited` or `init`, then
            this method raises a `RuntimeError` if the `_inited` attribute is `False`.

            Args:
                name: The name of the attribute being accessed.

            Returns:
                The value of the attribute.

            Raises:
                RuntimeError: If the Proxy has not been initialized and the attribute
                being accessed is not `_inited` or `init`.
            """
            if not name in ["_inited", "init"]:
                if not self._inited:
                    raise RuntimeError("Proxy not yet initialized")
            return super().__getattribute__(name)

        def init(self, *args, **kwargs):
            """
            Initializes the Proxy by initializing the underlying instance.

            Args:
                *args: Positional arguments to be passed to the parent class.
                **kwargs: Keyword arguments to be passed to the parent class.
            """
            super().__init__(*args, **kwargs)
            self._inited = True

    return Proxy
