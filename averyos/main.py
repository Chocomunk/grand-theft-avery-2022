from shell.shell import Shell
from puzzle.test_puzzle1 import test_puzzle1


if __name__ == '__main__':
    root = test_puzzle1()
    shell = Shell(root)

    running = True
    while running:
        running = shell.handle_input(input(shell.prompt()))
