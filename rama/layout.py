class Layout():
    """
    Base class for layouts. This is here to enforce behavior all
    layouts should support.
    """

    def handle_command(self, **kw):
        raise NotImplementedError

    def activate(self, dispatcher):
        dispatcher.register('layout', self.handle_command)
    
    def deactivate(self, dispatcher):
        dispatcher.unregister(self.handle_command)
    
    def arrange(self):
        raise NotImplementedError

    def add(self, client):
        raise NotImplementedError

    def remove(self, client):
        raise NotImplementedError

    def focus(self, client):
        raise NotImplementedError

def layout(cls, *args, **kw):
    def setup(geom):
        return cls(geom, *args, **kw)
    return setup
