import os
import sys


class Logger:

    def __init__(self):
        # Stores tuples of (msg, log_type)
        #   Log type can be one of ["stdout", "stderr"]
        self._log = []      

    def clear(self):
        """ Clears the log and screen """
        os.system('cls' if os.name=='nt' else 'clear')
        self._log.clear()

    def log(self, msg, file=sys.stdout):
        """ Logs a message to stdout. Use `file=None` for silent log """
        self._log.append((str(msg), "stdout"))
        if file:
            print(msg, file=file)

    def logerr(self, msg, file=sys.stderr):
        """ Logs a message to stderr. Use `file=None` for silent log """
        self._log.append((str(msg), "stderr"))
        if file:
            print(msg, file=file)

    def get(self, start_i):
        """ Returns all logs starting from `start_i` onwards """
        return self._log[start_i:]

    def get_latest(self):
        """ Returns the latest log entry """
        return self.get(-1)
