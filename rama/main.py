import os
import xcb
import xcb.xproto
from rama import window_manager

import sys
import traceback

class main(object):
    def __init__(self, config):
        self.conn = xcb.connect(display=os.environ['DISPLAY'])
        self.wm = window_manager.WindowManager(conn)

    def run(self):
        wm.start_managing()

        # Main loop
        while True:
            try:
                event = conn.wait_for_event()
            except xcb.ProtocolException, error:
                print "Protocol error %s received!" % error.__class__.__name__
                traceback.print_exc(file=sys.stdout)
            except Exception, error:
                print "Unexpected error received: %s" % error.message
                traceback.print_exc(file=sys.stdout)
                break
            winman.handle_event(event)

        conn.disconnect()

if __name__ == '__main__':
    run()
