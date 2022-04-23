import os
import sys

from enum import Enum


class LogType(Enum):
    OUT="out"
    ERR="err"


STDOUT = sys.stdout         # Save stdout before we mess with it
STDERR = sys.stderr         # Save stdout before we mess with it


# TODO: test that the array stays alive
def make_stdout_stderr():
    stdout_log = Logger(STDOUT)
    stderr_log = Logger(STDERR, logarr=stdout_log._log, logtype=LogType.ERR)
    return stdout_log, stderr_log


# TODO: Handle detached newlines
class Logger(object):
    """ 
    Creates a logger that writes to a file and saves the messages on memory
    
    Setting `file=None` will save messages without writing to a file.
    """

    def __init__(self, file, logarr=[], logtype=LogType.OUT):
        # Stores tuples of (msg, log_type)
        self._log = logarr
        self.logtype = logtype
        self.file = file

    def write(self, msg):
        if self.file:
            self.file.write(msg)
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
