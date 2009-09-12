class Geom(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return "x:%4d y:%4d w:%4d h:%4d" % (self.x, self.y, self.width, self.height)

    def copy(self):
        return Geom(self.x, self.y, self.width, self.height)
