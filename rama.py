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
    'M-n': cmd.send('layout next'),
    'M-S-p': views.select_prev,
    'M-S-n': views.select_next,
    'M-v': cmd.send('view test one two three'),
    'M-1': closure(views.select_index, 0),
    'M-2': closure(views.select_index, 1),
    'M-3': closure(views.select_index, 2),
    'M-4': closure(views.select_index, 3)
}

event.register_all(evd)

# TODO Clean this up
keys = Keymap(wm.conn, bindings)
keys.grab(wm.conn, wm.root.root)
evd.register('key_press', keys.handle)

views.set_default('www', 'code', 'comm', 'sys')
views.select_name('www')

app.run()
