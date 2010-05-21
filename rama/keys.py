from xcb.xproto import ModMask, GrabMode
from keysymdef import keysyms
from keysyms import Keysyms, keysym_to_str, keysym_to_char

masks = [ModMask.Shift,
         ModMask.Lock,
         ModMask.Control,
         ModMask._1,
         ModMask._2,
         ModMask._3,
         ModMask._4,
         ModMask._5]

modstrs = {'C': ModMask.Control,
           'S': ModMask.Shift,
           'M': ModMask._1,
           's': ModMask._5}

class KeyParseError(Exception):
    pass

def parse(keystr):
    """
    Parse a keystring.
    Returns a (modmask, keycode) tuple.
    """
    modmask = 0
    keys = keystr.split('-')
    for mod in keys[:-1]:
        if mod not in modstrs:
            raise KeyParseError()
        modmask = modmask | modstrs[mod]
    key = keys[-1:][0]
    if key not in keysyms:
        raise KeyParseError()
    return (modmask, keysyms[key])

def get_numlock_mask(conn):
    syms = Keysyms(conn)
    numlock = syms.get_keycode(keysyms['Num_Lock'])
    modmap = conn.core.GetModifierMapping().reply()
    for i in range(8):
        for j in range(modmap.keycodes_per_modifier):
            keycode = modmap.keycodes[i * modmap.keycodes_per_modifier + j]
            if keycode == numlock:
                return masks[i]
    return 0

class Keymap(object):
    bindings = {}

    def __init__(self, conn, keys=None):
        if keys is None:
            keys = {}
        self.numlockmask = get_numlock_mask(conn)
        self.syms = Keysyms(conn)
        for keystr in keys:
            self.bind(keystr, keys[keystr])

    def bind(self, keystr, action):
        key = parse(keystr)
        self.bindings[key] = action
        print "bound %s" % keystr

    def grab(self, conn, root):
        modifiers = [0, ModMask.Lock, self.numlockmask, 
                     self.numlockmask | ModMask.Lock]
        for key in self.bindings:
            for mod in modifiers:
                keycode = self.syms.get_keycode(key[1])
                conn.core.GrabKey(True, root, key[0] | mod, keycode,
                                  GrabMode.Async, GrabMode.Async)

    def ungrab(self, conn, root):
        modifiers = [0, ModMask.Lock, self.numlockmask, 
                     self.numlockmask | ModMask.Lock]
        for key in self.bindings:
            for mod in modifiers:
                conn.core.UngrabKey(key[1], root, key[0] | mod)

    def handle(self, keypress):
        keysym = self.syms.get_keysym(keypress.detail, 0)
        mask = self.cleanmask(keypress.state)
        for key in self.bindings:
            if mask == self.cleanmask(key[0]) and keysym == key[1]:
                self.bindings[key]()

    def cleanmask(self, mask):
        return mask & ~(self.numlockmask | ModMask.Lock)
