import os

from system.filesystem import Node, File


def make_graph(dirnames, adj_mat):
    """
    Builds a graph from the directory names and adjacency matrix.
    (row, col) -> (parent, child)
    """
    n = len(dirnames)
    if len(set(dirnames)) != n:
        raise ValueError("Duplicate directory name")
    
    nodes = [Node(dirname=name) for name in dirnames] 
    for i in range(n):
        parent = nodes[i]
        for j in range(n):
            if adj_mat[i][j]:
                parent.add_child(nodes[j])
                nodes[j].add_parent(parent)

    return {dirnames[i]: nodes[i] for i in range(n)}


def add_dir_files(node: Node, dirname):
    """ Adds all files in the real directory to the AveryOS node directory """
    for filename in os.listdir(dirname):
        if '.' in filename:
            f = File(filename, filepath=os.path.join(dirname, filename))
            node.directory.add_file(f)
