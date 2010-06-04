import os
from rama.event import EventController
from rama.window_manager import WindowManager
import xcb
import xcb.xproto


class main(object):
    def __init__(self, config):
        conn = xcb.connect(display=os.environ['DISPLAY'])
        self.wm = WindowManager(conn, config)
        self.xec = EventController(self.wm)

    def run(self):
        # TODO Replace with init dispatch
        self.wm.start_managing()

        # Main loop
        while True:
            self.xec.dispatch_events()

        self.conn.disconnect()
