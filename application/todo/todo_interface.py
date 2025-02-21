from abc import ABC

from infrastructure.json.todo_storage import save_todo, load_todo, append_todo, delete_todo, update_todo


class TodoInterface(ABC):
    def save(self, objects):
        save_todo(objects)

    def load(self):
        return load_todo()

    def append(self, objects):
        append_todo(objects)

    def delete(self, key, value):
        return delete_todo(key, value)

    def get(self, data, key, value):
        for obj in data:
            if obj[key] == value:
                return obj
        return None

    def update(self, todo):
        return update_todo(todo)
