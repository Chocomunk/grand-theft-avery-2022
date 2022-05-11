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
    data = LinesLog()
    stdout_log = CopyLogger(STDOUT, logdata=data, logtype=LogType.OUT)
    stderr_log = CopyLogger(STDERR, logdata=data, logtype=LogType.ERR)
    stdin_log = CopyLogger(STDIN, logdata=data, logtype=LogType.IN)
    return stdout_log, stderr_log, stdin_log


class LinesLog:
    """
    Maintains an array of all lines of strings written. Automatically splits
    string into different lines.
    """

    def __init__(self, lines=[]):
        self.lines = lines
        self.curr_line = ""

    # Convert '\n' and '\t' to new line entries and spaces.
    def write(self, msg, logtype=LogType.OUT):
        lines = msg.split('\n')
        self.curr_line += lines[0]
        for line in lines[1:]:
            self.curr_line = self.curr_line.replace('\t', "    ")
            self.lines.append((self.curr_line, logtype))
            self.curr_line = line

    def __len__(self):
        return len(self.lines)

    def getlines(self, start_i=0, end_i=None):
        """ Returns all logs in `[start_i:end_i]` """
        if not end_i:
            return self.lines[start_i:]
        return self.lines[start_i:end_i]

    def get_curr_line(self):
        """ Returns the text in the current line """
        return self.curr_line

    def flush(self):
        pass


class CopyLogger(object):
    """ 
    Copies all written messages to memory while still writing to the file.
    
    Setting `file=None` will save messages without writing to a file.
    """

    def __init__(self, file, logdata: LinesLog=LinesLog(), logtype=LogType.OUT):
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
        self.log.flush()
