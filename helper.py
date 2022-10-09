import csv
import json
import logging
import os
from typing import List


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


def read_file(filename: str):
    if not exists(filename):
        return None
    with open(filename) as f:
        return json.load(f)


def __clean_data(x):
    del x['meta']
    del x['uid']
    return x


def format_output(followers, following):
    # intersection
    for uid in followers.keys():
        followers[uid]["following"] = uid in following
    # sort
    sorted_followers = sorted(followers.values(), key=lambda user: user.get("follower_count") or 0, reverse=True)
    # format output
    return [__clean_data(x) for x in sorted_followers]


def write_csv(filename: str, data: List[dict]):
    if len(data) == 0:
        logging.error("no data to write")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)