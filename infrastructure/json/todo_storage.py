from infrastructure.json.helper import save_to_file, load_file, init_file, append_to_file, delete_from_file

FILENAME = 'todo.json'


def save_todo(objects):
    save_to_file(objects, FILENAME)


def load_todo():
    return load_file(FILENAME)


def append_todo(new_objects):
    append_to_file(new_objects, FILENAME)


def delete_todo(key, value):
    return delete_from_file(key, value, FILENAME)


def init_todo():
    init_file(FILENAME)


def update_todo(todo):
    todos, error = load_file(FILENAME)
    for index, obj in enumerate(todos):
        if obj['title'] == todo['title']:
            todos[index] = todo
            save_to_file(todos, FILENAME)
            return todo, None
    return None, 'Task not found'

