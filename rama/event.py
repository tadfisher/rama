from rama.dispatch import Dispatcher
import re
import traceback
import sys
import xcb
from xcb import xproto


CAPITAL_LETTER_RE = re.compile(r'\B([A-Z])')


class EventDispatcher(Dispatcher):
    def __init__(self, wm):
        super(EventDispatcher, self).__init__(wm=wm)
        self.conn = wm.conn

    def dispatch_events(self):
        try:
            event = self.conn.wait_for_event()
            if (event):
                self.dispatch_event(event)
        except xcb.ProtocolException, error:
            print "Protocol error %s received!" % error.__class__.__name__
            traceback.print_exc(file=sys.stdout)
        except Exception, error:
            print "Unexpected error received: %s" % error.message
            traceback.print_exc(file=sys.stdout)

    def dispatch_event(self, event):
        evname = CAPITAL_LETTER_RE.sub(
            '_\\1', event.__class__.__name__[:-5]).lower()
        
        # self.dispatch('before_%s' % evname, event=event)
        self.dispatch(evname, event=event)
        # self.dispatch('after_%s' % evname, event=event)


def destroy_notify(**kw):
    wm = kw['wm']
    event = kw['event']
    client = wm.win_to_client(event.window)
    if not client: return
    wm.unmanage_client(client)


def enter_notify(**kw):
    wm = kw['wm']
    event = kw['event']
    if event.mode is not xproto.NotifyMode.Normal: return
    client = wm.win_to_client(event.event)
    if not client: 
        return
    wm.focus(client)


def focus_in(**kw):
    wm = kw['wm']
    event = kw['event']
    win = event.event        # Weird, I know.
    if wm.sel_client and win != wm.sel_client.win:
        self.conn.core.SetInputFocus(
            xproto.InputFocus.PointerRoot, 
            win, 
            xproto.Time.CurrentTime)


def map_request(**kw):
    wm = kw['wm']
    event = kw['event']
    if wm.win_to_client(event.window):
        return
    wm.manage_window(event.window)


def unmap_notify(**kw):
    wm = kw['wm']
    event = kw['event']
    client = wm.win_to_client(event.window)
    if not client: return
    wm.unmanage_client(client)


def register_all(dispatcher):
    for evname in ("destroy_notify enter_notify focus_in map_request"
                   " unmap_notify").split():
        func = globals().get(evname)
        if func:
            dispatcher.register(evname, func)
