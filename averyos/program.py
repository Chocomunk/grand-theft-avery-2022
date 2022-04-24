from enum import Enum
from abc import ABC, abstractmethod


class ExitCode(Enum):
    OK = 0
    ERROR = 1
    EXIT = -1


class ProgramBase(ABC):

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    @abstractmethod
    def gui_main(self, args) -> ExitCode:
        pass


class CLIProgramBase(ProgramBase):

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    # GUI interface is just the text intergface
    def gui_main(self, args):
        return self.cli_main()
