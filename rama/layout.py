from frame import *

class Layout(object):
    """
    Base class for layouts. This is here to enforce behavior all
    layouts should support.
    """
    def arrange(self):
        raise NotImplementedError

    def add(self, client):
        raise NotImplementedError

    def remove(self, client):
        raise NotImplementedError

    def focus(self, client):
        raise NotImplementedError
