import abc
import six
from gi.repository import Gtk, GObject
from gi.types import GObjectMeta


class WidgetPageMeta(GObjectMeta, abc.ABCMeta):
    pass


class WidgetPage(six.with_metaclass(WidgetPageMeta, Gtk.ScrolledWindow)):
    def __init__(self, controller):
        super(WidgetPage, self).__init__(hscrollbar_policy=Gtk.PolicyType.NEVER)
        self.vbox = Gtk.Box(valign=Gtk.Align.START,
                            orientation=Gtk.Orientation.VERTICAL,
                            border_width=5)
        self.add(self.vbox)

        self.widgets = {}
        self.controller = controller
        self.controller.connect('device-added', self.on_device_added)

    def add_to_notebook(self, notebook):
        notebook.append_page(self,
                             Gtk.Label(label=self.notebook_label))

    @abc.abstractproperty
    def notebook_label(self):
        pass

    @abc.abstractmethod
    def get_widget(self, device):
        return None

    def on_device_added(self, controller, device):
        widget = self.get_widget(device)
        if widget:
            self.vbox.pack_start(widget, False, False, 5)
            self.vbox.show_all()
            self.widgets[device] = widget
            self.resort_device(device)
            device.connect('device-removed', self.on_device_removed)

    def resort_device(self, device):
        widget = self.widgets[device]
        sorted_widgets = sorted(self.widgets.values(),
                                key=lambda widget: widget.device.sort_key)
        self.vbox.reorder_child(widget, sorted_widgets.index(widget))

    def on_device_removed(self, device):
        if device in self.widgets:
            self.vbox.remove(self.widgets.pop(device))
