from enum import Enum
from abc import ABC, abstractmethod


class ExitCode(Enum):
    OK = 0
    ERROR = 1
    EXIT = -1


class ProgramBase(ABC):

    def __init__(self, hidden=False):
        self.hidden = hidden

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    @abstractmethod
    def gui_main(self, gui, args) -> ExitCode:
        pass


class CLIProgramBase(ProgramBase):

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    # GUI interface is just the text interface
    def gui_main(self, gui, args):
        return self.cli_main(args)
