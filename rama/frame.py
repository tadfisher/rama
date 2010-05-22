"""
Various frame classes intended to provide both floating and tiled
client positioning.
"""

from __future__ import division

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

    def __len__(self):
        if self.child:
            return 1
        return 0

    def debug(self, indent=0):
        for i  in range(indent):
            print '\t',
        print "Frame"
        print self.child.debug(indent+1)

    def redisplay(self):
        """
        Applies current geometry to child element, if it exists.
        """
        if self.child:
            self.child.geom = self.geom.copy()
            self.child.redisplay()

    def contains(self, frame):
        """
        Return True if this frame contains the requested child.
        """
        if self.child == frame:
            return True
        return False

    def find(self, client):
        """
        Return the Frame containing client.
        """
        if self.child == client:
            return self
        return None

class SplitFrame(Frame):
    """
    Base class for split frames. Maintains ratios of child elements
    and operations on those ratios.
    """

    def __init__(self, geom, children=None):
        """
        Initialize a SplitFrame with a geometry and a list of children.
        @param geom: initial geometry of the frame
        @type geom: Geom
        @param children: list of child frames and/or clients
        @type children: list
        """
        Frame.__init__(self, geom)
        if children is None:
            self.children = []
        else:
            self.children = children
        self.ratios = {}
        self.balance()
        self.geom = geom.copy()

    def __len__(self):
        return len(self.children)

    def debug(self, indent=0):
        for i in range(indent):
            print '\t',
        print self.__class__.__name__
        for child in self.children:
            child.debug(indent+1)

    def balance(self):
        """
        Equalize ratios among child frames.
        """

        n = len(self.children)
        if n == 0:
            return
        q = 10000 // n
        r = 10000 % q
        for c in self.children:
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

    def add(self, frame):
        n = len(self.children)
        if n == 0:
            self.ratios[frame] = 10000
        elif n == 1:
            self.ratios[self.children[0]] = 5000
            self.ratios[frame] = 5000
        else:
            q = 10000 // (n+1)
            t = 10000 - q
            for child in self.children:
                self.ratios[child] = int((self.ratios[child] / 10000) * t)
            self.ratios[frame] = q
        self.children.append(frame)

    def replace(self, frame, newframe):
        index = self.children.index(frame)
        self.children.remove(frame)
        self.children.insert(index, newframe)

    def remove(self, frame):
        """
        Attempt to remove the specified frame at the lowest level in
        the SplitFrame hierarchy.
        """

        #TODO make pixel-perfect
        for i,child in enumerate(self.children):
            if child == frame:
                self.children.remove(child)
                del self.ratios[child]
                n = len(self.children)
                t = sum(self.ratios.values())
                for c, r in self.ratios.items():
                    self.ratios[c] = int((r / t) * 10000)
            elif child.contains(frame):
                child.remove(frame)

    def contains(self, frame):
        """
        Return True if any child contains the specified frame.
        """
        for child in self.children:
            if child.contains(frame):
                return True
        return False

    def find(self, client):
        """
        Return the containing frame of client.
        """
        for child in self.children:
            if child.contains(client):
                return child.find(client)
        return None

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

    def __init__(self, geom, children=None):
        """
        Initialize the frame with a geometry and a list of children.
        @param geom: initial geometry of the frame 
        @type geom: Geom
        @param children: a list of initial clients and/or frames, in
        display order.  
        @type children: list
        """

        super(VSplitFrame, self).__init__(geom, children)

    def redisplay(self):
        """
        Recursively set the dimensions of child frames according to
        the vertical split algorithm.
        """

        cur_y = 0
        for c in self.children:
            c.geom.x = self.geom.x
            c.geom.y = cur_y
            c.geom.width = self.geom.width
            c.geom.height = (self.ratios[c] * self.geom.height) // 10000
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

    def __init__(self, geom, children=None):
        """
        Initialize the frame with a geometry and a list of children.
        @param geom: initial geometry of the frame 
        @type geom: Geom
        @param children: a list of initial clients and/or frames, in
        display order.  
        @type children: list
        """

        super(HSplitFrame, self).__init__(geom, children)

    def redisplay(self):
        """
        Recursively set the dimensions of child frames according to
        the horizontal split algorithm.
        """

        cur_x = 0
        for c in self.children:
            c.geom.x = cur_x
            c.geom.y = self.geom.y
            c.geom.width = (self.ratios[c] * self.geom.width) // 10000
            c.geom.height = self.geom.height
            c.redisplay()
            cur_x += c.geom.width
