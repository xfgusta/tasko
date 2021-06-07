from gi.repository import Gtk, Gdk, GLib

from gettext import gettext as _

from .define import UI_PATH, TASK_FILE
from .database import Database


@Gtk.Template(resource_path=f'{UI_PATH}/window.ui')
class TaskoWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'TaskoWindow'

    task_db = Database(TASK_FILE)

    menu_button = Gtk.Template.Child()
    task_entry = Gtk.Template.Child()
    task_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        builder = Gtk.Builder.new_from_resource(f'{UI_PATH}/menu.ui')
        menu = builder.get_object('menu')
        popover = Gtk.Popover.new_from_model(self.menu_button, menu)
        self.menu_button.set_popover(popover)

        tasks = self.task_db.read_data()
        for task, done in tasks.items():
            self.add_task_to_list(task, done)
            self.task_db.task_history.append(task)

    @Gtk.Template.Callback()
    def on_task_entry_changed(self, task_entry):
        task = task_entry.get_text().strip()
        if task and task not in self.task_db.task_history:
            task_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,
                                               'value-increase-symbolic')
        else:
            task_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,
                                               None)

    @Gtk.Template.Callback()
    def on_task_entry_enter_pressed(self, task_entry, event):
        if event.keyval == Gdk.KEY_Return:
            self.add_task(task_entry)

    @Gtk.Template.Callback()
    def on_task_entry_icon_pressed(self, task_entry, cursor_pos, event):
        self.add_task(task_entry)

    def on_task_check_toggled(self, task_check, task_label):
        task = task_label.get_text()
        done = task_check.get_active()
        self.update_task_status(task, task_check, task_label, done)
        self.task_db.update_task_status(task, done)

    def on_task_delete_pressed(self, task_check, event, task):
        self.delete_task(task)

    def add_task_to_list(self, task, done=False):
        task_row = self.make_task_row(task, done)
        self.task_list.insert(task_row, -1)
        self.task_list.show_all()

    def add_task(self, task_entry, done=False):
        task = task_entry.get_text().strip()
        if task and task not in self.task_db.task_history:
            self.add_task_to_list(task, done)
            self.task_db.add_task(task)
            task_entry.set_text('')

    def delete_task(self, task):
        i = self.task_db.task_history.index(task)
        task_row = self.task_list.get_row_at_index(i)
        self.task_list.remove(task_row)
        self.task_db.delete_task(task)

    def delete_completed_tasks(self):
        history = self.task_db.task_history
        for i in reversed(range(len(history))):
            task_row = self.task_list.get_row_at_index(i)
            task_check = task_row.get_child().get_children()[0]
            if task_check.get_active():
                self.task_list.remove(task_row)
                self.task_db.delete_task(history[i])

    def delete_all_tasks(self):
        history = self.task_db.task_history
        for i in reversed(range(len(history))):
            task_row = self.task_list.get_row_at_index(i)
            self.task_list.remove(task_row)
            self.task_db.delete_task(history[i])

    def update_task_status(self, task, task_check, task_label, done):
        if done:
            task_label.set_markup(f'<s>{task}</s>')
            task_check.set_tooltip_text(_('Unmark as done'))
        else:
            task_label.set_text(task)
            task_check.set_tooltip_text(_('Mark as done'))

    def make_task_row(self, task, done=False):
        builder = Gtk.Builder.new_from_resource(f'{UI_PATH}/task_row.ui')
        task_row = builder.get_object('task_row')
        task_check = builder.get_object('task_check')
        task_label = builder.get_object('task_label')
        task_delete = builder.get_object('task_delete')

        task_check.set_active(done)
        self.update_task_status(task, task_check, task_label, done)

        builder.connect_signals({
            'on_task_check_toggled': (self.on_task_check_toggled, task_label),
            'on_task_delete_pressed': (self.on_task_delete_pressed, task)})

        return task_row
