"""
Provides the log search and goto line functionality 
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5.QtGui import QIntValidator
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from enum import Enum, auto

from Operations.config import Config

class State(Enum):
    GOTO_LINE = auto()
    SEARCH = auto()

class OpenLogsSearchOps(QtWidgets.QLineEdit):

    goto_line = QtCore.pyqtSignal(int)
    search = QtCore.pyqtSignal(str)
    search_prev = QtCore.pyqtSignal(str)

    def __init__(self, openLogsSearch, globalInformationOps):
        QtWidgets.QLineEdit.__init__(self, openLogsSearch)

        self.global_information_ops = globalInformationOps
        self.local_state = State.SEARCH
        self.int_validator = QIntValidator()

        config = Config()
        open_logs_search_style = config.array_config_str('open_logs_search_style')
        if open_logs_search_style:
            self.setStyleSheet(open_logs_search_style)

    def run_selected(self, number):
        """ Run the operation of the selected history """
        if len(self.prev_data) >= number:
            self.setText(str(self.prev_data[number]))
            self.process_ops_input()

    def init_goto_line(self):
        """ Set the input state for a numeric entry indicating the log line to jump to """
        self.local_state = State.GOTO_LINE
        self.setFocus()
        self.setValidator(self.int_validator)

    def init_search_log(self):
        """ Set the input state for text entry indicating the regex to search for in the log """
        self.local_state = State.SEARCH
        self.setFocus()
        self.setValidator(None)

    def process_ops_input(self):
        """ Process a goto line or text search query """
        input_data = self.text()
        if (self.local_state == State.GOTO_LINE):
            self.goto_line.emit(int(input_data))
        else:
            self.search.emit(input_data)

    def process_search_prev(self):
        """ Fire signal with search of a regex in the search history """
        input_data = self.text()
        self.search_prev.emit(input_data)

    def process_goto_history_data(self, goto_history):
        """ Display the history of the goto line values """
        info_prev_data = 'Mode: goto line'
        self.prev_data = goto_history
        if goto_history:
            info_prev_data = info_prev_data + ' - '
            count = 0
            for data in goto_history:
                info_prev_data = info_prev_data + str(count) + ") " + str(data) + " "
                count = count + 1

        self.global_information_ops.display_info(info_prev_data)
    
    def process_search_history_data(self, search_history):
        """ Display the history of the log search values """
        info_prev_data = 'Mode: search'
        self.prev_data = search_history
        if search_history:
            info_prev_data = info_prev_data + ' - '
            count = 0
            for data in search_history:
                info_prev_data = info_prev_data + str(count) + ") " + str(data) + " "
                count = count + 1

        self.global_information_ops.display_info(info_prev_data)

