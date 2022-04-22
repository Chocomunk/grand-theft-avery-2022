from shell import Shell
from filesystem_gen import test_filesystem1


if __name__ == '__main__':
    root = test_filesystem1()
    shell = Shell(root)

    running = True
    while running:
        running = shell.handle_input(input(shell.prompt()))
