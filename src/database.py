import json
import os
import sys


class Database:
    __gtype_name__ = 'Database'

    task_history = []

    def __init__(self, task_file):
        self.task_file = task_file

    def add_task(self, task, done=False):
        data = self.read_data()
        data[task] = done
        self.save_data(data)
        self.task_history.append(task)

    def delete_task(self, task):
        data = self.read_data()
        del data[task]
        self.save_data(data)
        self.task_history.remove(task)

    def update_task_status(self, task, done=False):
        data = self.read_data()
        data[task] = done
        self.save_data(data)

    def read_data(self):
        data = {}

        try:
            with open(self.task_file, 'r') as f:
                data = json.load(f)
        except IOError:
            os.makedirs(os.path.dirname(self.task_file), exist_ok=True)
            self.save_data({})
        except Exception as e:
            print(e, file=sys.stderr)
            exit(1)

        return data

    def save_data(self, data):
        try:
            with open(self.task_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(e, file=sys.stderr)
            exit(1)
