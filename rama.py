#!/usr/bin/env python
from rama import layout, main

defaults = {
    'layouts': [layout.TileLayout()],
    'views': ['main']
}

if __name__ == '__main__':
    main.run(defaults)
