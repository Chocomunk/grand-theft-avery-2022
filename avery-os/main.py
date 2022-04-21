from shell import Shell
from filesystem import test_filesystem1


if __name__ == '__main__':
    root = test_filesystem1()
    sh = Shell(root)

    running = True
    while running:
        running = sh.handle_input(input(sh.prompt()))