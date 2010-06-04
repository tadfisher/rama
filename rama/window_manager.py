from rama.client import Client
from rama.dispatch import Dispatcher
from rama.keys import Keymap
from rama.util import Geom
from rama.view import View
import re
from xcb import xproto
from xcb.xproto import EventMask


CAPITAL_LETTER_RE = re.compile(r'\B([A-Z])')

WM_EV_MASK = (
    EventMask.EnterWindow          | 
    EventMask.FocusChange          |
    EventMask.KeyPress             |
    EventMask.LeaveWindow          |
    EventMask.PropertyChange       | 
    EventMask.SubstructureNotify   |
    EventMask.SubstructureRedirect)


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

        # Keybindings
        self.keymap = Keymap(conn, config['keys'])
        
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
        self.keymap.grab(self.conn, self.root.root)
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
        value_list = [
            EventMask.EnterWindow    | 
            EventMask.FocusChange    |
            EventMask.PropertyChange |
            EventMask.StructureNotify
            ]
        self.conn.core.ChangeWindowAttributes(win, value_mask, value_list)
        self.conn.core.MapWindow(win)
        self.sel_view.add_client(client)
        self.sel_view.redisplay()
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

    def handle_event(self, event):
        evname = CAPITAL_LETTER_RE.sub(
            '_\\1', event.__class__.__name__[:-5]).lower()
        if hasattr(self, evname):
            handle = getattr(self, evname)
            handle(event)

    # Event handlers

    def configure_notify(self, event):
        # Use to detect when to resize root win
        # Oh, and floating windows too :)
        pass

    def destroy_notify(self, event):
        client = self.win_to_client(event.window)
        if not client: return
        self.unmanage_client(client)

    def enter_notify(self, event):
        if event.mode is not xproto.NotifyMode.Normal: return
        client = self.win_to_client(event.event)
        if not client: 
            return
        self.focus(client)

    def focus_in(self, event):
        if self.sel_client and event.event != self.sel_client.win:
            self.conn.core.SetInputFocus(
                xproto.InputFocus.PointerRoot, 
                event.event, 
                xproto.Time.CurrentTime)

    def key_press(self, event):
        self.keymap.handle(event)

    def map_request(self, event):
        if self.win_to_client(event.window):
            return
        client = self.manage_window(event.window)

    def unmap_notify(self, event):
        client = self.win_to_client(event.window)
        if not client: return
        self.unmanage_client(client)

