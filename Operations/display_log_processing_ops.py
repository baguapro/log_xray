"""
Provides all the operations of the logs being displayed
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5 import QtCore, QtGui

import pandas as pd
import threading
import re

from Operations.read_logfile_ops import ReadLogFileOps
from Operations.highlighter import Highlighter
from Operations.config import Config

class DisplayLogProcessingOps(QtCore.QThread):

    def __init__(self,logFileLocation, logTextDisplay, parent=None):
        super(DisplayLogProcessingOps, self).__init__(parent)

        self.log_file_location = logFileLocation
        self.log_text_display = logTextDisplay

        self.search_history = []
        self.goto_line_history = []
        self.log_filters = dict() 

        # cache the log lines internally with a pandas Dataframe
        self.log_df = pd.DataFrame(columns=['line_number','log_line'])

        self.init_read_logfile()

        config = Config()
        style_str = config.array_config_str('log_display_style')
        if style_str:
            self.log_text_display.getTextEdit().setStyleSheet(style_str);

        log_processing_config = config.get_config(self.log_file_location)
        if log_processing_config:
            self.search_history = log_processing_config['search_history']
            self.goto_line_history = log_processing_config['goto_line_history']
            self.log_filters = log_processing_config['log_filters']

        # init the text highlighting class
        self.highlighter = Highlighter(self.log_text_display.getTextEdit().document())

        self.lock = threading.Lock()

    def init_read_logfile(self):
        """
        Create the object that reads the log file data and link to the log line 
        processing method
        """
        self.read_logfile_ops = ReadLogFileOps(self.log_file_location)
        self.read_logfile_ops.log_line.connect(self.process_log_line)

    def refresh_data(self):
        """ Clear all data and re-init the read log file ops object """
        self.read_logfile_ops.stop()
        self.read_logfile_ops = None

        self.lock.acquire()
        try:
            self.log_df = self.log_df.iloc[0:0]
            self.log_text_display.getTextEdit().clear()
            self.init_read_logfile()

        finally:
            self.Lock.release()

    def filter_log(self, refresh=True, log_line=''):
        """
        filter the log data with the applied filters.
        refresh: True - (default) filter the log data with the applied filters and display
        refresh: False - display log_line if its not filtered out or if no filters are applied
        log_line: - log line data to be displayed if not filtered out
        """
        self.lock.acquire()

        try:
            if refresh:
                if self.log_filters:
                    filtered_df = pd.DataFrame(columns=['line_number','log_line'])

                    # get only the log lines that pass filtering
                    for key, log_filter in self.log_filters.items():
                        filtered_df = filtered_df.append(
                                self.log_df[self.log_df.log_line.str.match(log_filter)]
                                )
                
                    # make sure data is in correct order
                    filtered_df.sort_values('line_number',inplace=True)

                    # display any log data not filtered out
                    if not filtered_df.empty:
                        self.log_text_display.refresh_data(filtered_df)

                else:
                    # no applied filter so display all log data
                    log_lines = self.log_df['log_line'].tolist()
                    self.log_text_display.reset_data()
                    for line in log_lines:
                        self.log_text_display.getTextEdit().append(line)

            else:
                # not refreshing so if log_line is not filtered out then append to output
                line_number = len(self.log_df.index) + 1
                self.log_df = self.log_df.append({'line_number':line_number,'log_line':log_line}, ignore_index=True)

                if self.log_filters:
                    for key, log_filter in self.log_filters.items():
                        if re.match(log_filter, log_line):
                            self.log_text_display.setOriginalLineNum(line_number)
                            self.log_text_display.getTextEdit().append(log_line)
                            break
                else:
                    # no applied filter so just append to output display
                    self.log_text_display.getTextEdit().append(log_line)
        finally:
            self.lock.release()



    def process_log_line(self, log_line):
        # forward log_line to filter_log method for processing
        self.filter_log(False,log_line)

    def run(self):
        """ Start the processing of this threaded class """
        self.read_logfile_ops.start()
      
    def goto_line(self, line_number):
        # add to history is not already in history cache
        if(line_number not in self.goto_line_history):
            self.goto_line_history.insert(0, line_number)
            if len(self.goto_line_history) > 10:
                del self.goto_line_history[-1]

            self.save_processing_data()

        # set the cursor to the requested line_number
        cursor = QtGui.QTextCursor(
                self.log_text_display.getTextEdit().document().findBlockByLineNumber(line_number - 1)
            )

        self.log_text_display.getTextEdit().setFocus()
        self.log_text_display.getTextEdit().setTextCursor(cursor)

    def search(self, search_str):
        # add to history if not already in history cache
        if(search_str not in self.search_history):
            self.search_history.insert(0,search_str)
            if len(self.search_history) > 10:
                del self.search_history[-1]

            self.save_processing_data()

        # make sure our log display widget has the focus and create the search regex
        self.log_text_display.getTextEdit().setFocus()
        search_regx = QtCore.QRegExp(search_str)
        found = True
        if(not self.log_text_display.getTextEdit().find(search_regx)):
            # search is performed from the current point in the displayed log data
            # onwards, if search_str regex not found loop back to the top of the doc
            # and start again
            found = False
            orig_cursor = self.log_text_display.getTextEdit().textCursor()

            cursor = QtGui.QTextCursor(
                self.log_text_display.getTextEdit().document().findBlockByLineNumber(0)
                )

            self.log_text_display.getTextEdit().setTextCursor(cursor)
            if( not self.log_text_display.getTextEdit().find(search_regx)):
                # if still not found set the display back to the original location
                self.log_text_display.getTextEdit().setTextCursor(orig_cursor)
            else:
                found = True

        if found:
            # highlight the search_str if found
            self.highlighter.add_search_highlight(search_str)

    def search_prev(self, search_str):
        """ Search for search_str backwards """
        self.log_text_display.getTextEdit().setFocus()
        search_regx = QtCore.QRegExp(search_str)
        flag = QtGui.QTextDocument.FindBackward

        if(not self.log_text_display.getTextEdit().find(search_regx, flag)):
            orig_cursor = self.log_text_display.getTextEdit().textCursor()

            cursor = QtGui.QTextCursor(
                self.log_text_display.getTextEdit().document().lastBlock()
                )

            self.log_text_display.getTextEdit().setTextCursor(cursor)
            if( not self.log_text_display.getTextEdit().find(search_regx, flag)):
                self.log_text_display.getTextEdit().setTextCursor(orig_cursor)
       
    def goto_line_info(self):
        """ Provide the goto line history """
        self.prev_data = []
        self.prev_data = self.goto_line_history[:9]
        return self.prev_data

    def search_info(self):
        """ Provide the search history """
        self.prev_data = []
        self.prev_data = self.search_history[:9]
        return self.prev_data

    def add_filter(self, filterItem):
        self.log_filters[filterItem.text()] = filterItem.statusTip()
        self.filter_log()

        self.save_processing_data()

    def remove_filter(self,filterItem):
        if filterItem.text() in self.log_filters:
            del self.log_filters[filterItem.text()]
            self.filter_log()

        self.save_processing_data()

    def tab_filters(self):
        return self.log_filters

    def get_logfile_location(self):
        return self.log_file_location

    def stop_processing(self):
        self.del_processing_data()
        self.read_logfile_ops.stop()
        self.terminate()

    def save_processing_data(self):
        log_processing_data = dict()
        log_processing_data['search_history'] = self.search_history
        log_processing_data['goto_line_history'] = self.goto_line_history
        log_processing_data['log_filters'] = self.log_filters

        config = Config()
        config.add_config_data(self.log_file_location, log_processing_data)
        config.save_config_data()

    def del_processing_data(self):
        config = Config()
        config.remove_config_data(self.log_file_location)
        config.save_config_data()
