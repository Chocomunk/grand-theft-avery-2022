from __future__ import annotations
from typing import Callable, List, Optional


class File:

    def __init__(self, filename, data):
        self.name = filename
        self.data = data


class Directory:

    def __init__(self, dirname):
        self.name = dirname
        self._data = {}     # May be able to turn this into a list

    def add_file(self, file: File):
        self._data[file.name] = file

    def list_dir(self):
        return list(self._data.keys())


def always_false(*args, **kwargs): return False

class Node:

    def __init__(self, parents=[], dirname="New Folder", directory: Directory=None):
        self.directory = Directory(dirname) if not directory else directory
        self.children = []

        # Callbacks
        self.entry_callbacks: List[Callable] = []

        # Locking
        # lockfunc should be called on the current node and the calling shell
        self.lockfunc: Callable[..., bool] = always_false
        self.passlocked = False
        self.password = None

        # Point to both children and parents for navigating.
        self.navref = {}
        for parent in parents:
            parent.add_child(self)

    # TODO: consider defining event/state objects to pass into callbacks
    def call_entry_callbacks(self, *args, **kwargs):
        """ Must be called when entering this node """
        for cb in self.entry_callbacks:
            cb(*args, **kwargs)
    
    def add_entry_callback(self, callback: Callable):
        self.entry_callbacks.append(callback)

    # TODO: consider defining event/state objects to pass into callbacks
    def locked(self, *args, **kwargs):
        return self.passlocked or self.lockfunc(*args, **kwargs)

    def set_lock(self, lockfunc: Callable[..., bool]):
        self.lockfunc = lockfunc

    def set_password(self, password):
        self.passlocked = True
        self.password = password

    def try_password(self, password):
        if not self.password or password == self.password:
            self.passlocked = False
            return True
        return False

    def add_child(self, child_node: Node):
        self.children.append(child_node)
        self.navref[child_node.directory.name] = child_node
        child_node.navref[self.directory.name] = self

    def find_neighbor(self, dirname) -> Optional[Node]:
        if dirname in self.navref:
            return self.navref[dirname]
        return None

    def list_children(self):
        return [c.directory.name for c in self.children]
        