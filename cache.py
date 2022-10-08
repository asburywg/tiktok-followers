import json
import os


def exists(filename: str):
    return os.path.exists(filename)


def append(filename: str, data: dict):
    # write empty json file if DNE
    if not exists(filename):
        with open(filename, 'w+') as f:
            f.write('{}')
    with open(filename) as f:
        contents = json.load(f)
    contents.update(data)
    with open(filename, 'w') as f:
        json.dump(contents, f)


def read(filename: str, key: str):
    if not exists(filename):
        return None
    with open(filename) as f:
        contents = json.load(f)
        return contents.get(key)
