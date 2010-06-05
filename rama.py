#!/usr/bin/env python
from rama import event
from rama.actions import launch
from rama.keys import Keymap
from rama.main import Main
from rama.layouts.tile import tile
from rama.util import closure
from rama.view_manager import ViewManager

app = Main()
wm = app.wm
cmd = app.cmd
evd = app.evd
layouts = [tile(nmaster=1)]
views = ViewManager(wm, cmd, layouts)

bindings = {
    'M-x': launch('xeyes'),
    'M-t': launch('xterm'),
    'M-space': launch('dmenu_run'),
    'M-n': cmd.send('layout next'),
    'M-S-p': views.select_prev,
    'M-S-n': views.select_next,
    'M-v': cmd.send('view test one two three'),
}

for i in range(9):
    bindings['M-%d' % (i+1)] = closure(views.select_index, i)

event.register_all(evd)

# TODO Clean this up
keys = Keymap(wm.conn, bindings)
keys.grab(wm.conn, wm.root.root)
evd.register('key_press', keys.handle)

views.set_default('www', 'code', 'comm', 'sys')
views.select_name('www')

app.run()
