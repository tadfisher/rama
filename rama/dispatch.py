class Dispatcher(object):
    """Event dispatching interface.
    """

    def __init__(self, **defaults):
        self.handlers = {}
        self.defaults = defaults

    def register(self, name, *chain):
        self.handlers.setdefault(name, []).append(chain)
        for f in chain:
            if hasattr(f, '__connected__'):
                f.__connected__(**self.defaults)

    def unregister(self, func):
        for chains in self.handlers.values():
            for i, chain in enumerate(chains):
                if func in chain:
                    chains.pop(i)

    def dispatch(self, name, **kw):
        kw_dict = dict(self.defaults, **kw)
        for chain in self.handlers.get(name, [])[:]:
            for func in chain:
                if not func(**kw_dict):
                    break
