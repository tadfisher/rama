"""
Various frame classes intended to provide both floating and tiled
client positioning.
"""

class Frame(object):
    """
    Frame for displaying a single child or no child (empty frame).
    """

    def __init__(self, geom, child=None):
        """
        Initializes a Frame with a geometry and an optional child frame.
        @param geom: initial geometry of the frame
        @type geom: Geom
        @param child: initial child frame or client
        @type child: Frame, Client
        """

        self.geom = geom.copy()
        self.child = child

    def redisplay(self):
        """
        Applies current geometry to child element, if it exists.
        """

        if self.child is not None:
            self.child.geom = self.geom.copy()
            self.child.redisplay()

class SplitFrame(Frame):
    """
    Base class for split frames. Maintains ratios of child elements
    and operations on those ratios.
    """

    def __init__(self, geom, children=[]):
        """
        Initialize a SplitFrame with a geometry and a list of children.
        @param geom: initial geometry of the frame
        @type geom: Geom
        @param children: list of child frames and/or clients
        @type children: list
        """

        Frame.__init__(self, geom)
        self.children = children
        self.ratios = {}
        self.balance()

    def balance(self):
        """
        Equalize ratios among child frames.
        """

        n = len(self.children)
        if n == 0:
            return
        q = 10000 / n
        r = 10000 % q
        for (i, c) in enumerate(self.children):
            if r > 0:
                self.ratios[c] = q + 1
                r -= 1
            else:
                self.ratios[c] = q

    def redisplay(self):
        """
        Recursively set the dimensions of child frames.  Implemented
        by subclass.
        """

        raise NotImplementedError

class VSplitFrame(SplitFrame):
    """
    Frame that arranges clients in a vertical stack.
    
    Example::

        +----+
        |    |
        +----+
        |    |
        +----+
    """

    def __init__(self, geom, children=[]):
        """
        Initialize the frame with a geometry and a list of children.
        @param geom: initial geometry of the frame 
        @type geom: Geom
        @param children: a list of initial clients and/or frames, in
        display order.  
        @type children: list
        """

        SplitFrame.__init__(self, geom, children)

    def redisplay(self):
        """
        Recursively set the dimensions of child frames according to
        the vertical split algorithm.
        """

        cur_y = 0
        for (i, c) in enumerate(self.children):
            c.geom.x = self.geom.x
            c.geom.y = cur_y
            c.geom.width = self.geom.width
            c.geom.height = (self.ratios[c] * self.geom.height) / 10000
            c.redisplay()
            cur_y += c.geom.height

class HSplitFrame(SplitFrame):
    """
    Frame that arranges clients in a horizontal stack.

    Example::
    
        +----+----+
        |    |    |
        +----+----+
    """

    def __init__(self, geom, children=[]):
        """
        Initialize the frame with a geometry and a list of children.
        @param geom: initial geometry of the frame 
        @type geom: Geom
        @param children: a list of initial clients and/or frames, in
        display order.  
        @type children: list
        """

        SplitFrame.__init__(self, geom, children)

    def redisplay(self):
        """
        Recursively set the dimensions of child frames according to
        the horizontal split algorithm.
        """

        cur_x = 0
        for (i, c) in enumerate(self.children):
            c.geom.x = cur_x
            c.geom.y = self.geom.y
            c.geom.width = (self.ratios[c] * self.geom.width) / 10000
            c.geom.height = self.geom.height
            c.redisplay()
            cur_x += c.geom.width
