from infrastructure.json.helper import save_to_file, load_file, init_file, append_to_file, delete_from_file

FILENAME = 'assignee.json'


def save_assignee(objects):
    save_to_file(objects, FILENAME)


def load_assignee():
    return load_file(FILENAME)


def append_assignee(new_objects):
    append_to_file(new_objects, FILENAME)


def delete_assignee(key, value):
    return delete_from_file(key, value, FILENAME)


def init_assignee():
    init_file(FILENAME)


def update_assignee(person):
    persons, error = load_file(FILENAME)
    for index, obj in enumerate(persons):
        if obj['name'] == person['name']:
            persons[index] = person
            save_to_file(persons, FILENAME)
            return person, None
    return None, 'Person not found'
