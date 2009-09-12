import frame

class Layout(object):
    def arrange(self, geom, clients=[]):
        raise NotImplementedError

class TileLayout(Layout):
    def __init__(self, nmaster=1):
        self.nmaster = nmaster
    
    def arrange(self, geom, clients=[]):
        n = len(clients)
        if n == 0:
            return frame.Frame(geom)
        if n <= self.nmaster:
            return frame.VSplitFrame(geom, clients)
        master = clients[:self.nmaster]
        stack = clients[self.nmaster:]
        return frame.HSplitFrame(geom,
                                 [frame.VSplitFrame(geom, master), 
                                  frame.VSplitFrame(geom, stack)])
