import layout

class View(object):
    def __init__(self, name, geom, layouts):
        self.name = name
        self.layouts = layouts
        self.clients = []
        self.geom = geom
        self.sel_layout = layouts[0]

    def redisplay(self):
        frame = self.sel_layout.arrange(self.geom, self.clients)
        frame.redisplay()
