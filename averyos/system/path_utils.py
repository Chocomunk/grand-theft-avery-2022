import re
import sys

from shell.env import ENV
from system.filesystem import File


def clean_path(s):
    return re.sub('//+', '/', s).strip('/')


def path_subdirs(dirname):
    dirname = clean_path(dirname)
    path = ENV.curr_node.find_node(dirname)

    if not path:
        pwd = ENV.curr_node.directory.name
        print("Error: could not find {0} under {1}".format(
            dirname, pwd), file=sys.stderr)
        return None

    for node in path:
        if node.locked():
            print("Error: {0} is locked!".format(node.directory.name))
            return None

    return path


def get_file(filepath) -> File | None:
    split = clean_path(filepath).rsplit('/', 1)
    filename = split[-1]                # Last entry is filename

    if len(split) > 1:
        path = path_subdirs(split[0])
        if not path:
            return None
        node = path[-1]            # Search under final node in path
    else:
        node = ENV.curr_node       # Default search in curr_node

    if filename not in node.directory.files:
        print("Error: no file named {0} in {1}".format(
            filename, node.directory.name), file=sys.stderr)
        return None

    return node.directory.files[filename]