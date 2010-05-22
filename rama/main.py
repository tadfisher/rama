import os
import xcb
import xcb.xproto
import wm

import sys
import traceback

def run(config):
    conn = xcb.connect(display=os.environ['DISPLAY'])
    winman = wm.WindowManager(conn, config)
    winman.start_managing()

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
