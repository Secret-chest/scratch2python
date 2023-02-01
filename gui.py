import gi
from subprocess import PIPE, Popen
from threading import Thread

from queue import Queue, Empty

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


p = Popen(['python', 'main.py'], stdout=PIPE, stdin=PIPE, bufsize=1, close_fds=True, universal_newlines=True)
q = Queue()
t = Thread(target=enqueue_output, args=(p.stdout, q))
t.daemon = True  # thread dies with the program
t.start()


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

if __name__ == '__main__':
    Gtk.main()
