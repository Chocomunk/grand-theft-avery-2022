from shell.shell import Shell
from puzzle.test_puzzle1 import test_puzzle1
import tkinter as tk
from terminal import Terminal


if __name__ == '__main__':
    # root = test_puzzle1()
    # shell = Shell(root)

    # running = True
    # while running:
    #     running = shell.handle_input(input(shell.prompt()))
    root = tk.Tk()
    terminal = Terminal(pady=5, padx=5, selectbackground='White')
    terminal.pack(expand=True, fill='both')
    # Don't want to run through our shell
    # terminal.shell = True

    terminal.basename = 'fuckyou$'



    root.mainloop()
