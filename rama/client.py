"""
Classes for managing X11 clients.
"""

import xcb
import xcb.xproto

class Client(object):
    """
    Class for managing X11 client windows.
    """

    def __init__(self, conn, win, geom):
        """
        Initialize managed client.
        @param geom: initial geometry of the client
        @param win: managed window
        """

        self.conn = conn
        self.geom = geom.copy()
        self.win = win

    def debug(self, indent=0):
        for i in range(indent):
            print '\t',
        print 'Window %x' % self.win

    def configure(self, **changes):
        value_mask = 0
        value_list = []
        for k in 'x', 'y', 'width', 'height':
            if k in changes:
                value_mask |= getattr(xcb.xproto.ConfigWindow, k.capitalize())
                value_list.append(changes[k])
        if value_mask:
            # Attempt to configure the window. If we can't, this
            # window must have been destroyed, and the WM must have
            # received the event.
            cookie = self.conn.core.ConfigureWindowChecked(self.win, value_mask, value_list)

    def redisplay(self):
        self.configure(x=self.geom.x, y=self.geom.y, 
                       width=self.geom.width, height=self.geom.height)

    def focus(sef):
        self.dpy
