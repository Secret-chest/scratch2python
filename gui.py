import gi
import os
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def pause(button):
    print("PAUSE", file=p.stdin)
    print("PAUSE")


def stop(button):
    print("STOP", file=p.stdin)
    print("STOP")


handlers = {
    "onDestroy": Gtk.main_quit,
    "pause": pause,
    "stop": stop,
}

builder = Gtk.Builder()
builder.add_from_file("main.glade")
builder.connect_signals(handlers)

window = builder.get_object("test")
window.show_all()

stdin  = sys.stdin.fileno() # usually 0
stdout = sys.stdout.fileno() # usually 1

parentStdin, childStdout  = os.pipe()
childStdin,  parentStdout = os.pipe()
pid = os.fork()
if pid:
    # parent process
    os.close(childStdout)
    os.close(childStdin)
    os.dup2(parentStdin, stdin)
    os.dup2(parentStdout, stdout)
    Gtk.main()
else:
    # child process
    os.close(parentStdin)
    os.close(parentStdout)
    os.dup2(childStdin, stdin)
    os.dup2(childStdout, stdout)
    os.execl("python", "main.py", "main.py")
