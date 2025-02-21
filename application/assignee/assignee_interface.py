from abc import ABC

from infrastructure.json.assignee_storage import save_assignee, load_assignee, append_assignee, delete_assignee, \
    update_assignee


class AssigneeInterface(ABC):
    def save(self, objects):
        save_assignee(objects)

    def load(self):
        return load_assignee()

    def append(self, objects):
        append_assignee(objects)

    def delete(self, key, value):
        return delete_assignee(key, value)

    def get(self, data, key, value):
        for obj in data:
            if obj[key] == value:
                return obj
        return None

    def update(self, person):
        return update_assignee(person)
