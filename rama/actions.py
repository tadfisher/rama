from os import fork, execvp

def launch(cmd):
    args = cmd.split()
    def launcher():
        if not fork():
            execvp(args[0], args)
    return launcher
