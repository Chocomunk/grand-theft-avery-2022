from __future__ import annotations
from typing import Optional


class File():

    def __init__(self, filename, data):
        self.name = filename
        self.data = data


class Directory():

    def __init__(self, dirname):
        self.name = dirname
        self._data = {}     # May be able to turn this into a list

    def add_file(self, file: File):
        self._data[file.name] = file

    def list_dir(self):
        return list(self._data.keys())


class Node():

    def __init__(self, parents=[], directory=None, dirname="New Folder"):
        self.directory = Directory(dirname) if not directory else directory
        self.children = []

        # Point to both children and parents for navigating.
        self.navref = {}
        for parent in parents:
            parent.add_child(self)

    def add_child(self, child_node: Node):
        self.children.append(child_node)
        self.navref[child_node.directory.name] = child_node
        child_node.navref[self.directory.name] = self

    def navigate(self, dirname) -> Optional[Node]:
        if dirname in self.navref:
            return self.navref[dirname]
        return None

    def list_children(self):
        return [c.directory.name for c in self.children]


def test_filesystem1():
    root = Node(dirname="root")
    a = Node(parents=[root], dirname="A")
    b = Node(parents=[a], dirname="B")
    c = Node(parents=[root, b], dirname="C")
    d = Node(parents=[a], dirname="D")
    c.add_child(root)
    d.add_child(root)

    shared = File("shared.txt", "shared text")
    a.directory.add_file(File("a.txt", "a text"))
    c.directory.add_file(shared)
    d.directory.add_file(shared)

    return root


if __name__=='__main__':
    root = test_filesystem1()

    print(root.navigate("C").directory.list_dir())
    print(root.navigate("A").navigate("D").directory.list_dir())
    print(root.navigate("C").navigate("root").directory.name)
