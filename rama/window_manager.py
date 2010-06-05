from rama.client import Client
from rama.dispatch import Dispatcher
from rama.keys import Keymap
from rama.util import Geom
from rama.view import View
from xcb import xproto
from xcb.xproto import EventMask


WM_EV_MASK = (
    EventMask.EnterWindow | 
    EventMask.FocusChange |
    EventMask.KeyPress |
    EventMask.LeaveWindow |
    EventMask.PropertyChange | 
    EventMask.SubstructureNotify |
    EventMask.SubstructureRedirect)

CLIENT_EV_LIST = [
            EventMask.EnterWindow | 
            EventMask.FocusChange |
            EventMask.PropertyChange |
            EventMask.StructureNotify]
    


class WindowManager(Dispatcher):
    clients = []
    focused = []
    views = []
    sel_client = None
    sel_view = None

    def __init__(self, conn, config):
        super(WindowManager, self).__init__(wm=self)

        self.conn = conn

        # Setup root window
        setup = conn.get_setup();
        self.root = root = setup.roots[conn.pref_screen]
        self.root_geom = Geom(0, 0, root.width_in_pixels, root.height_in_pixels)

        # Setup views
        for name in config['views']:
            self.views.append(View(name, self.root_geom, config['layouts']))
        self.sel_view = self.views[0]

    def start_managing(self):
        # Select for WM events
        cookie = self.conn.core.ChangeWindowAttributesChecked(
            self.root.root, 
            xproto.CW.EventMask, 
            [WM_EV_MASK])
        try:
            cookie.check()
        except xproto.BadAccess:
            raise Exception("Another window manager is already running.")
        self.scan_for_clients()
        
    def stop_managing(self):
        self.keymap.ungrab(self.conn, self.root.root)
        conn.disconnect()

    def scan_for_clients(self):
        tree = self.conn.core.QueryTree(self.root.root).reply()
        for win in tree.children:
            self.manage_window(win)

    # Actions

    def focus(self, client):
        if self.sel_client:
            self.unfocus(sel.client)
        if client in self.focused:
            self.focused.remove(client)
        self.focused.append(client)
        self.conn.core.SetInputFocus(
            xproto.InputFocus.PointerRoot,
            client.win, 
            xproto.Time.CurrentTime)
        self.conn.flush()

    def unfocus(self, client):
        self.conn.core.SetInputFocus(
            xproto.InputFocus.PointerRoot, 
            self.root.root, 
            xproto.Time.CurrentTime)

    def manage_window(self, win):
        if win == self.root.root: return
        if self.win_to_client(win): return

        self.dispatch('before_manage_window', win=win)

        get_geom = self.conn.core.GetGeometry(win).reply()
        geom = Geom(get_geom.x, get_geom.y, get_geom.width, get_geom.height)
        client = Client(self.conn, win, geom)
        self.clients.append(client)

        # Select for client events
        value_mask = xproto.CW.EventMask
        self.conn.core.ChangeWindowAttributes(win, value_mask, CLIENT_EV_LIST)

        self.sel_view.add_client(client)
        self.sel_view.redisplay()
        self.conn.core.MapWindow(win)
        self.conn.flush()

        self.dispatch('after_manage_window', win=win, client=client)

        return client
    
    def unmanage_client(self, client):
        for view in self.views:
            if client in view.clients:
                view.remove_client(client)
        self.clients.remove(client)
        self.sel_view.redisplay()
        self.conn.flush()

    def win_to_client(self, win):
        for client in self.clients:
            if client.win == win:
                return client
        return None
