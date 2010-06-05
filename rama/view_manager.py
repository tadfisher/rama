from rama.util import OrderedDict
from rama.view import View

class ViewManager(object):
    def __init__(self, wm, cmd, layouts):
        self.wm = wm
        self.cmd = cmd
        self.views = OrderedDict()
        self.default_names = []
        self.layouts = layouts
        self.geom = wm.root_geom
        self.selected = None

        wm.register('after_manage_window', self.manage_client)
        wm.register('before_unmanage_client', self.unmanage_client)
        cmd.register('view', self.command)

    def set_default(self, *names):
        self.default_names = []
        for name in names:
            self.default_names.append(name)
            self.add(name)

    def add(self, name):
        if name not in self.views.keys():
            self.views[name] = View(self.cmd, self.geom, self.layouts)
        if len(self.views) == 1:
            self.select_name(name)
            
    def remove(self, name):
        if len(self.views) > 1:
            if name in self.views and name not in self.default_names:
                self.views.pop(name, None)
            # TODO Change to focus stack
            self.select_name(self.views.keys[0])
        # TODO signal error for no such view

    # Actions

    def select_name(self, name):
        if name not in self.views.keys():
            # signal error
            return
        if self.selected in self.views.keys():
            self.views[self.selected].deactivate()
        self.selected = name
        self.views[self.selected].activate()
        self.wm.flush()

    def select_index(self, index):
        if len(self.views) == 1:
            return
        if index < 0 or index > len(self.views)-1:
            return
        names = self.views.keys()
        name = names[index]
        self.select_name(name)

    def select_prev(self):
        if len(self.views) == 1:
            return
        names = self.views.keys()
        i = names.index(self.selected)
        name = names[(i-1) % len(self.views)]
        self.select_name(name)
        self.wm.flush()

    def select_next(self):
        if len(self.views) == 1:
            return
        names = self.views.keys()
        i = names.index(self.selected)
        name = names[(i+1) % len(self.views)]
        self.select_name(name)

    def manage_client(self, **kw):
        self.views[self.selected].add_client(kw['client'])
        self.views[self.selected].redisplay()
        kw['wm'].flush()

    def unmanage_client(self, **kw):
        for view in self.views.values():
            view.remove_client(kw['client'])
        self.views[self.selected].redisplay()
        kw['wm'].flush()

    def command(self, **kw):
        args = kw['args']

        if len(args) == 0: return
        if args[0] == 'refresh':
            self.views[self.selected].redisplay()
            self.wm.flush()
