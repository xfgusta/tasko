import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

from gettext import gettext as _

from .window import TaskoWindow
from .define import APP_ID, UI_PATH


class Application(Gtk.Application):
    def __init__(self, version):
        super().__init__(application_id=APP_ID,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.version = version
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        delete_completed = Gio.SimpleAction.new('delete_completed', None)
        delete_completed.connect('activate', self.on_delete_completed_tasks)
        self.add_action(delete_completed)

        delete_all = Gio.SimpleAction.new('delete_all', None)
        delete_all.connect('activate', self.on_delete_all_tasks)
        self.add_action(delete_all)

        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self.on_about)
        self.add_action(about)

    def do_activate(self):
        self.window = self.props.active_window

        if not self.window:
            self.window = TaskoWindow(application=self)

        self.window.present()

    def on_delete_completed_tasks(self, action, param):
        self.window.delete_completed_tasks()

    def on_delete_all_tasks(self, action, param):
        self.window.delete_all_tasks()

    def on_about(self, action, param):
        builder = Gtk.Builder.new_from_resource(f'{UI_PATH}/about.ui')
        about_dialog = builder.get_object("about_dialog")
        about_dialog.set_transient_for(self.window)
        about_dialog.set_version(self.version)
        about_dialog.present()


def main(version):
    app = Application(version)
    return app.run(sys.argv)
