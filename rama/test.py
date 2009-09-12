import client
import frame
import layout
import wm
import util
import xcb, xcb.xproto

def wm_setup(display=':0'):
    conn = xcb.connect(display=display)
    winman = wm.WindowManager(conn)
    winman.start_managing()
    return winman


if __name__ == '__main__':
    test = Test()
    test.tile()

