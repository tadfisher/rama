import os
import xcb
import xcb.xproto
import wm

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
            break
        except:
            print "Unexpected error received: %s" % error.message
            break
        winman.handle_event(event)


    conn.disconnect()

if __name__ == '__main__':
    run()


