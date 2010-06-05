#!/usr/bin/env python
from rama import event
from rama.actions import launch
from rama.keys import Keymap
from rama.main import main
from rama.layouts.tile import tile


def hello_world(**kw):
    print 'YAY!!!!'

config = {
    'layouts': [tile(nmaster=2)],
    'views': ['main'],
    }

app = main(config)
wm = app.wm
cmd = app.cmd
evd = app.evd

bindings = {
    'M-x': launch('xeyes'),
    'M-t': launch('xterm'),
    'M-n': cmd.send('layout next')
}

keys = Keymap(wm.conn, bindings)
keys.grab(wm.conn, wm.root.root)

event.register_all(evd)
evd.register('key_press', keys.handle)

app.run()
