import json

import os


def save_to_file(objects, filename):
    path = os.path.join('appdir', filename)
    try:
        with open(path, 'w', encoding='utf-8') as json_file:
            json.dump(objects, json_file, indent=2, ensure_ascii=True)
    except (IOError, TypeError) as e:
        print(f"An error occurred while saving to JSON: {e}")


def append_to_file(new_objects, filename):
    existing_data, is_valid = load_file(filename)
    existing_data.append(new_objects.to_dict())
    save_to_file(existing_data, filename)


def delete_from_file(key, value, filename):
    objects, is_valid = load_file(filename)
    deleted = False
    for i in range(len(objects)):
        if objects[i][key] == value:
            objects.pop(i)
            deleted = True
    save_to_file(objects, filename)
    return deleted


def load_file(filename):
    path = os.path.join('appdir', filename)
    try:
        with open(path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            return existing_data, False
    except (IOError, TypeError) as e:
        return [], True


def init_file(filename):
    dir = init_directory()
    file_path = os.path.join(dir, filename)

    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as json_file:
                json.dump([], json_file)
        except IOError as e:
            print(f"An error occurred while creating the JSON file: {e}")


def init_directory():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    directory = os.path.join(root, 'appdir')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
