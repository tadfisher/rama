import layout

class View(object):
    def __init__(self, cmd, geom, layouts):
        self.cmd = cmd
        self.geom = geom
        self.layouts = []
        self.clients = []
        for setup in layouts:
            self.layouts.append(setup(geom))
        self.sel_layout = self.layouts[0]

    def activate(self):
        self.sel_layout.activate(self.cmd)
        self.redisplay()

    def deactivate(self):
        self.sel_layout.deactivate(self.cmd)
        for client in self.clients:
            client.hide()
        
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

