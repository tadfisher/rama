from rama.dispatch import Dispatcher

class CommandDispatcher(Dispatcher):
    def __init__(self, wm):
        super(CommandDispatcher, self).__init__(wm=wm,cmd=self)

    def send(self, command):
        args = command.split()
        def closure():
            self.dispatch('%s' % args[0], args=args[1:])
        return closure

    def send_now(self, command):
        args = command.split()
        self.dispatch('%s' % args[0], args=args[1:])
