import pygame
import os
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GdkX11

class GameWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        vbox = Gtk.VBox(False, 2)
        vbox.show()
        self.add(vbox)

        #create the menu
        file_menu = Gtk.Menu()

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        dialog_item = Gtk.MenuItem()
        dialog_item.set_label("Dialog")
        dialog_item.show()
        dialog_item.connect("activate",self.show_dialog)
        file_menu.append(dialog_item)
        dialog_item.show()

        quit_item = Gtk.MenuItem()
        quit_item.set_label("Quit")
        quit_item.show()
        quit_item.connect("activate",self.quit)
        file_menu.append(quit_item)
        quit_item.show()

        menu_bar = Gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        file_item = Gtk.MenuItem()
        file_item.set_label("_File")
        file_item.set_use_underline(True)
        file_item.show()

        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)

        #create the drawing area
        da = Gtk.DrawingArea()
        da.set_size_request(300,300)
        da.show()
        vbox.pack_end(da, False, False, 0)
        da.connect("realize",self._realized)

        #set up the pygame objects
        self.image = pygame.image.load("sprite.png")
        self.background = pygame.image.load("background.png")
        self.x = 150
        self.y = 150

        #collect key press events
        self.connect("key-press-event", self.key_pressed)

    def key_pressed(self, widget, event, data=None):
        if event.keyval == 65361:
            self.x -= 5
        elif event.keyval == 65362:
            self.y -= 5
        elif event.keyval == 65363:
            self.x += 5
        elif event.keyval == 65364:
            self.y += 5

    def show_dialog(self, widget, data=None):
        #prompts.info("A Pygtk Dialog", "See it works easy")
        title = "PyGame embedded in Gtk Example"
        dialog = Gtk.Dialog(title, None, Gtk.DialogFlags.MODAL,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        content_area = dialog.get_content_area()
        label = Gtk.Label("See, it still works")
        label.show()
        content_area.add(label)
        response = dialog.run()
        dialog.destroy()

    def quit(self, widget, data=None):
        self.destroy()

    def draw(self):
        self.screen.blit(self.background,[0,0])

        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        self.screen.blit(self.image, rect)
        pygame.display.flip()

        return True

    def _realized(self, widget, data=None):
        os.putenv('SDL_WINDOWID', str(widget.get_window().get_xid()))
        pygame.init()
        pygame.display.set_mode((300, 300), 0, 0)
        self.screen = pygame.display.get_surface()
        GObject.timeout_add(200, self.draw)

if __name__ == "__main__":
    window = GameWindow()
    window.connect("destroy",Gtk.main_quit)
    window.show()
    Gtk.main()
