#!/usr/bin/env python
from rama.main import main
from rama.layouts.tile import tile
from rama.actions import launch


def hello_world(**kw):
    print 'YAY!!!!'

config = {
    'layouts': [tile(nmaster=2)],
    'views': ['main'],
    'keys': {
        'M-x': launch('xeyes'),
        'M-t': launch('xterm'),
        }
    }

app = main(config)

wm = app.wm


app.run()
