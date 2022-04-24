from __future__ import annotations
from typing import Callable, Dict, List, Optional


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

    # Static variables
    next_id = 0         # Keeps track of the next available unique-id
    id_to_node: List[Node] = []

    def __init__(self, parents: List[Node]=[], dirname="New Folder", 
                directory: Directory=None, master=False):
        # Set unique id
        self.id = Node.next_id
        Node.next_id += 1

        # Assign or create new directory
        self.directory = Directory(dirname) if not directory else directory

        # Callbacks
        # All callbacks and lock functions should idealling use ENV and a 
        # puzzle-specific state to manage data. Need to change the implementation
        # here if that is not possible.
        # Callbacks should be called on the containing node
        self.entry_callbacks: List[Callable[[Node]]] = []

        # Locking
        # lockfunc should be called on the containing node
        self.lockfunc: Callable[[Node], bool] = always_false
        self.passlocked = False
        self.password = None

        # Node connections (children/parents)
        # Point to both children and parents for navigating.
        self.navref: Dict[str, Node] = {}
        self.children: List[Node] = []
        self.parents: List[Node] = parents
        for parent in parents:
            parent.add_child(self)

        # Add node to id_to_node map
        Node.id_to_node.append(self)

    def call_entry_callbacks(self):
        """ Must be called when entering this node """
        for cb in self.entry_callbacks:
            cb(self)
    
    def add_entry_callback(self, callback: Callable):
        self.entry_callbacks.append(callback)

    def locked(self):
        return self.passlocked or self.lockfunc(self)

    def set_lock_func(self, lockfunc: Callable[..., bool]):
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
        