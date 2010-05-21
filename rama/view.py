import layout

class View(object):
    def __init__(self, name, geom, layouts):
        self.name = name
        self.geom = geom
        self.layouts = []
        self.clients = []

        for setup in layouts:
            self.layouts.append(setup(geom))

        self.sel_layout = self.layouts[0]

    def redisplay(self):
        frame = self.sel_layout.arrange()
        frame.redisplay()

    def add_client(self, client):
        if client not in self.clients:
            self.clients.append(client)
        for layout in self.layouts:
            layout.add(client)

    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
        for layout in self.layouts:
            layout.remove(client)
