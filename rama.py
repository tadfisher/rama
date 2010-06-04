#!/usr/bin/env python
from rama import main
from rama.layouts.tile import tile
from rama.actions import launch

config = {
    'layouts': [tile(nmaster=1)],
    'views': ['main'],
    'keys': {
        'M-x': launch('xeyes'),
        'M-t': launch('xterm'),
        }
    }

main.run(config)
