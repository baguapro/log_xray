"""
Threaded class to tail the provided logfile and signal the log data
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5 import QtCore

import time


class ReadLogFileOps(QtCore.QThread):

    log_line = QtCore.pyqtSignal(str)

    def __init__(self, logfile, parent=None):
        super(ReadLogFileOps, self).__init__(parent)

        self.logfile = logfile
        self.opened_file = open(self.logfile, 'r')

        self.running = True

    def tail(self, file):
        """
        Continuously read lines from the given file, note that the file will have to
        be re-opend and read from again if the application writing to the file stops
        and reopens the file for writing.
        """
        line=''
        while self.running:
            tmp =  file.readline()
            if tmp:
                line += tmp
                if line.endswith("\n"):
                    yield line
                    line = ''

            else:
                time.sleep(0.5)
           
    def run(self):
        """ Start the thread running """
        for line in self.tail(self.opened_file):
            self.log_line.emit(line.strip('\n'))

    def stop(self):
        self.running= False
        self.opened_file.close()
        self.terminate()
