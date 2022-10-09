import csv
import json
import logging
import os
from typing import List
from pathlib import Path


def verify(filename: str):
    """
    Create directory for file if it doesn't exist
    :param filename: path to file
    :return: filename
    """
    if not exists(filename):
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
    return filename


def exists(filename: str):
    """
    Checks whether filename path exists
    :param filename: path to file
    :return: boolean
    """
    return os.path.exists(filename)


def append(filename: str, data: dict):
    """
    Updates or initializes json file
    :param filename: path to file
    :param data: dict data to append
    """
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
    """
    Reads key from json file
    :param filename: path to file
    :param key: value to retrieve
    :return: value of key in file or None
    """
    if not exists(verify(filename)):
        return None
    with open(filename) as f:
        contents = json.load(f)
        return contents.get(key)


def read_file(filename: str):
    """
    Reads entire json file
    :param filename: path to file
    :return: dict data
    """
    if not exists(filename):
        return None
    with open(filename) as f:
        return json.load(f)


def __clean_data(x):
    """
    helper function to format dict data for output
    :param x: dict of user
    :return: cleaned dict
    """
    del x['meta']
    del x['uid']
    return x


def format_output(followers, following):
    """
    Transforms data for output, add `following` field, sort followers by `follower_count`, remove extra fields
    :param followers: map of followers {uid: {...}}
    :param following: map of following {uid: {...}}
    :return: list of cleaned followers dict
    """
    # intersection
    for uid in followers.keys():
        followers[uid]["following"] = uid in following
    # sort
    sorted_followers = sorted(followers.values(), key=lambda user: user.get("follower_count") or 0, reverse=True)
    # format output
    return [__clean_data(x) for x in sorted_followers]


def write_csv(filename: str, data: List[dict]):
    """
    output CSV of data
    :param filename: path to file
    :param data: dict of payload
    """
    if len(data) == 0:
        logging.error("no data to write")
        return
    keys = data[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
