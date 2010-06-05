import os
from rama.command import CommandDispatcher
from rama.event import EventDispatcher
from rama.view_manager import ViewManager
from rama.window_manager import WindowManager
import xcb
import xcb.xproto


class Main(object):
    def __init__(self):
        conn = xcb.connect(display=os.environ['DISPLAY'])
        self.wm = WindowManager(conn)
        self.cmd = CommandDispatcher(self.wm)
        self.evd = EventDispatcher(self.wm)

    def run(self):
        # TODO Replace with init dispatch
        self.wm.start_managing()

        # Main loop
        while True:
            self.evd.dispatch_events()

        self.conn.disconnect()
