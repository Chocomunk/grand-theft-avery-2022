from __future__ import annotations
from typing import Callable, Dict, List, Optional

from system.program import ProgramBase


# TODO: Check filepath extension to see if file is an image
class File:

    def __init__(self, filename, data=None, filepath=None, is_image=False):
        self.name = filename
        self.data = data
        self.filepath = filepath
        self.is_image = is_image

    def get_data(self):
        if self.is_image:
            return "(this is an image...)"

        if not self.filepath:
            data = self.data
        else:
            with open(self.filepath, 'r') as f:
                data = f.read()

        if not data:
            return "(empty file...)"
        return data


class Directory:

    def __init__(self, dirname):
        self.name = dirname
        self.files: Dict[str, File] = {}
        self.programs: Dict[str, ProgramBase] = {}

    def add_file(self, file: File):
        self.files[file.name] = file

    def add_program(self, name, prog: ProgramBase):
        self.programs[name] = prog

    def list_files(self):
        return list(self.files.keys())

    def list_programs(self):
        return list(self.programs.keys())


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
        print(password, self.password.replace(" ", ""))
        if not self.password or password == self.password.replace(" ", ""):
            self.passlocked = False
            return True
        return False

    def add_child(self, child_node: Node):
        self.children.append(child_node)
        self.navref[child_node.directory.name] = child_node
        child_node.navref[self.directory.name] = self

    def find_neighbor(self, dirname) -> Optional[Node]:
        """ Returns a neighbor to this node if it exists. Else, return None """
        if dirname in self.navref:
            return self.navref[dirname]
        return None

    def find_node(self, dirname) -> List[Node]:
        """ 
        Returns a path to the final node in `dirname`. If no path exists, return
        an empty list
        """
        return self.find_node_recurse([], dirname.split('/'))

    def find_node_recurse(self, nodes, dirnames) -> Optional[Node]:
        depth = len(nodes)
        nodes.append(self)
        if depth == len(dirnames):
            return nodes

        dname = dirnames[depth]
        if dname in self.navref:
            return self.navref[dname].find_node_recurse(nodes, dirnames)
        return []

    def list_children(self):
        return [c.directory.name for c in self.children]
        