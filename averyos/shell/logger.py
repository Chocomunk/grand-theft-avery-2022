import sys

from enum import Enum
from typing import IO


class LogType(Enum):
    OUT = "out"
    ERR = "err"
    IN  = "in"


STDOUT = sys.__stdout__         # Save stdout before we mess with it
STDERR = sys.__stderr__         # Save stdout before we mess with it
STDIN  = sys.__stdin__          # Save stdin before we mess with it


def get_stdio_loggers():
    data = LogData()
    stdout_log = Logger(STDOUT, logdata=data, logtype=LogType.OUT)
    stderr_log = Logger(STDERR, logdata=data, logtype=LogType.ERR)
    stdin_log = Logger(STDIN, logdata=data, logtype=LogType.IN)
    return stdout_log, stderr_log, stdin_log


class LogData:

    def __init__(self, lines=[]):
        self.lines = lines
        self.curr_line = ""

    def write(self, msg, logtype):
        self.curr_line += msg
        if self.curr_line.endswith('\n'):
            self.lines.append((self.curr_line[:-1], logtype))
            self.curr_line = ""

    def get(self, start_i):
        """ Returns all logs starting from `start_i` onwards """
        return self.lines[start_i:]

    def get_latest(self):
        """ Returns the latest log entry """
        return self.get(-1)

    def get_curr_line(self):
        """ Returns the text in the current line """
        return self.curr_line


class Logger(object):
    """ 
    Creates a logger that writes to a file and saves the messages on memory
    
    Setting `file=None` will save messages without writing to a file.
    """

    def __init__(self, file, logdata: LogData=LogData(), logtype=LogType.OUT):
        # Stores tuples of (msg, log_type)
        self.log = logdata
        self.logtype: LogType = logtype
        self.file: IO = file

    def write(self, msg):
        if self.file:
            self.file.write(msg)
        self.log.write(msg, self.logtype)

    def readline(self):
        inp = self.file.readline()
        self.log.write(inp, self.logtype)
        return inp

    def flush(self):
        self.file.flush()
