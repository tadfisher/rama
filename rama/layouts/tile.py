from rama.layout import Layout
from rama.frame import *

class Tile(Layout):
    """
    DWM-style layout mode. Arranges windows in "master" and "stack"
    columns.
    """

    nmaster = 1                 # Maximum no. of clients in master

    def __init__(self, geom, **kw):
        self.geom = geom
        if 'nmaster' in kw:
            self.nmaster = kw['nmaster']
        self.master = VSplitFrame(self.geom)
        self.stack = VSplitFrame(self.geom)
        self.root = HSplitFrame(self.geom, [self.master])

    def debug(self):
        self.root.debug()
    
    def arrange(self):
        return self.root

    def add(self, client):
        client_frame = Frame(self.geom, client)
        if len(self.master) == self.nmaster:
            if len(self.stack) == 0:
                self.root.add(self.stack)
                self.root.balance()
            self.master.remove(self.focused_master)
            self.master.add(client_frame)
            self.stack.add(self.focused_master)
            self.focused_stack = self.focused_master
            self.focused_master = client_frame
        else:
            self.master.add(client_frame)
            self.focused_master = client_frame

    def remove(self, client):
        client_frame = self.root.find(client)
        if not client_frame:
            return
        if self.master.contains(client):
            self.master.remove(client_frame)
            if len(self.stack):
                self.stack.remove(self.focused_stack)
                self.master.add(self.focused_stack)
                self.focused_master = self.focused_stack
                if len(self.stack):
                    self.focused_stack = self.stack.children[0]
                else:
                    self.root.remove(self.stack)
        elif self.stack.contains(client):
            client_frame = self.stack.find(client)
            self.stack.remove(client_frame)
            if len(self.stack.children):
                if self.focused_stack == client_frame:
                    self.focused_stack = self.stack.children[0]
            else:
                self.root.remove(self.stack)
    
    def focus(self, client):
        pass

    def focus_next(self):
        pass

    def focus_prev(self):
        pass

    def focus_left(self):
        pass

    def focus_right(self):
        pass
    
    def zoom(self, client):
        pass

def tile(**kw):
    def setup(geom):
        return Tile(geom, **kw)
    return setup
