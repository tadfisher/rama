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
        print 'len(self.master) = %d' % len(self.master)
        print 'len(self.stack) = %d' % len(self.stack)
    
    def arrange(self):
        return self.root

    def add(self, client):
        print 'adding window to layout'
        print 'before add:'
        self.debug()
        client_frame = Frame(self.geom, client)
        # if len(self.master) == self.nmaster:
        #     if len(self.stack) == 0:
        #         self.root.add(self.stack)
        #         self.root.balance()
        #     self.master.remove(self.focused_master)
        #     self.master.add(client_frame)
        #     self.stack.add(self.focused_master)
        #     self.focused_stack = self.focused_master
        #     self.focused_master = client_frame
        # else:
        #     self.master.add(client_frame)
        #     self.focused_master = client_frame
        print 'after add:'
        self.master.add(client_frame)
        self.debug()

    def remove(self, client):
        print 'removing window from layout'
        print 'before remove:'
        self.debug()
        # if self.master.contains(client):
        #     print 'master contains client'
        #     client_frame = self.master.find(client)
        #     print 'client frame: %s' % client_frame
        #     self.master.remove(client_frame)
        #     if len(self.stack):
        #         self.stack.remove(self.focused_stack)
        #         self.master.add(self.focused_stack)
        #         self.focused_master = self.focused_stack
        #         if len(self.stack):
        #             self.focused_stack = self.stack.children[0]
        #         else:
        #             self.root.remove(stack)
        # elif self.stack.contains(client):
        #     print 'stack contains client'
        #     print 'client frame: %s' % client_frame
        #     client_frame = self.stack.find(client)
        #     self.stack.remove(client_frame)
        #     if focused_stack == client_frame:
        #         focused_stack = self.stack.children[0]
        client_frame = self.master.find(client)
        self.master.remove(client_frame)
        print 'removed window from layout'
        print 'after remove:'
        self.debug()
    
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
