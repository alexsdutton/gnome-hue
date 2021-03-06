from gi.repository import Gtk, Gio

from .window import MainWindow


class GHueApplication(Gtk.Application):
    def __init__(self, controller):
        super(GHueApplication, self).__init__(application_id="com.github.alexsdutton.gnome_hue",
                                              flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.controller = controller
        self.connect("activate", self.on_activate)

    def on_activate(self, data=None):
        window = MainWindow(self.controller)
        window.connect('destroy-event', Gtk.main_quit)
        window.show_all()
        self.add_window(window)