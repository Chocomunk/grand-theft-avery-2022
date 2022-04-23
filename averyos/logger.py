import os
import sys

from enum import Enum
from typing import IO, List


class LogType(Enum):
    OUT="out"
    ERR="err"


STDOUT = sys.stdout         # Save stdout before we mess with it
STDERR = sys.stderr         # Save stdout before we mess with it


def make_stdout_stderr():
    stdout_log = Logger(STDOUT)
    stderr_log = Logger(STDERR, logarr=stdout_log._log, logtype=LogType.ERR)
    return stdout_log, stderr_log


class Logger(object):
    """ 
    Creates a logger that writes to a file and saves the messages on memory
    
    Setting `file=None` will save messages without writing to a file.
    """

    def __init__(self, file, logarr=[], logtype=LogType.OUT):
        # Stores tuples of (msg, log_type)
        self._log: List = logarr
        self.logtype: LogType = logtype
        self.file: IO = file

    def write(self, msg):
        if self.file:
            self.file.write(msg)
        if msg != '\n':             # Newlines are written by themselves.
            self._log.append((str(msg), self.logtype))

    def flush(self):
        self.file.flush()

    def log_cli(self, msg):
        """ Logs a cli command.
        
        Calling `input(s)` will print "s" first without waiting for the input.
        We should overwrite that first print to include the input
        """
        self._log[-1] = ((str(msg), self.logtype))

    def get(self, start_i):
        """ Returns all logs starting from `start_i` onwards """
        return self._log[start_i:]

    def get_latest(self):
        """ Returns the latest log entry """
        return self.get(-1)
