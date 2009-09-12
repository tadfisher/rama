"""
vowm is the View-Oriented Window Manager.

vowm is a tiling window manager optimized for laptops with small
displays. It aims to combine the ease-of-use of the traditional WIMP
design with the flexibility of today's tiling window managers. In
addition, it shall provide both the manual-tiling paradigm (Ion,
Ratpoison, StumpWM) and the dynamic paradigm (dwm, xmonad, wmii).

What sets vowm apart is its take on the multiple-workspace
paradigm. Rather than having a distinct one-to-one mapping between
windows and workspaces, vowm allows users to create "views", which
allow windows to appear on multiple workspaces and in different
positions on each workspace. Windows are made available in a global
pool, and are selectable by the user for inclusion/exclusion from the
current view. Views may be created and destroyed on the fly.

"""

__author__ = 'Tad Fisher <tadfisher@gmail.com>'
"""The primary author of vowm."""

__license__ = 'DWTFYW'

__url__ = 'http://vowm.ghettodojo.com'
"""The vowm project's (current) homepage."""

__version__ = '0.1'
