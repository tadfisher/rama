from rama.frame import *
from rama.layout import Layout

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
        self.focused_master = None
        self.focused_stack = None
        self.focused = None

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
            self.focus(client_frame)
        else:
            self.master.add(client_frame)
            self.focus(client_frame)
            
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
                    self.focus(self.stack.children[0])
                else:
                    self.root.remove(self.stack)
            if not len(self.master):
                self.focused_master = None
                self.focused_stack = None
                self.focused = None
        elif self.stack.contains(client):
            client_frame = self.stack.find(client)
            self.stack.remove(client_frame)
            if len(self.stack.children):
                if self.focused_stack == client_frame:
                    self.focus(self.stack.children[0])
            else:
                self.root.remove(self.stack)

    def handle_command(self, **kw):
        args = kw['args']
        wm = kw['wm']
        cmd = kw['cmd']

        if len(args) == 0: return
        if args[0] == 'zoom':
            if self.focused:
                self.zoom(self.focused.child)
                cmd.send_now('view refresh')

        if len(args) == 1: return
        if args[0] == 'focus':
            if args[1] == 'next':
                self.focus_next()
            elif args[1] == 'prev':
                self.focus_prev()
            elif args[1] == 'left':
                self.focus_left()
            elif args[1] == 'right':
                self.focus_right()

        if len(args) == 2: return
        if args[0] == 'focus':
            if args[1] == 'client':
                win = int(args[2])
                client = wm.win_to_client(win)
                if client:
                    self.focus(client)
    
    def focus(self, client):
        client_frame = self.root.find(client)
        if not client_frame: return
        self.focused = client_frame
        if self.master.contains(client_frame):
            self.focused_master = client_frame
        elif self.stack.contains(client_frame):
            self.focused_stack = client_frame
        client_frame.child.focus()

    def focus_next(self):
        if not self.focused: return
        client_frame = self.root.find(self.focused)
        next = client_frame.next_sibling()
        if not next:
            if self.master.contains(self.focused) and len(self.stack):
                next = self.stack.at_index(0)
            else:
                next = self.master.at_index(0)
        if not next: return
        self.focus(next)

    def focus_prev(self):
        if not self.focused: return
        client_frame = self.root.find(self.focused)
        prev = client_frame.prev_sibling()
        if not prev:
            if self.stack.contains(self.focused):
                prev = self.master.at_index(len(self.master)-1)
            else:
                prev = self.stack.at_index(len(self.stack)-1)
        if not prev: return
        self.focus(prev)

    def focus_left(self):
        self.focus(self.focused_master)

    def focus_right(self):
        if len(self.stack):
            self.focus(self.focused_stack)
    
    def zoom(self, client):
        self.remove(client)
        self.add(client)
