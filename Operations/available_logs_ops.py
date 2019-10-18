"""
Generates a list of log files based on all the listed directories entered in the 
Log locations dialog
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


import os
import glob
import ntpath
import re

from PyQt5.QtWidgets import QListWidgetItem
from Operations.config import Config

class AvailableLogsOps():
    def __init__(self, availablelogsfilter, availablelogs):
        self.available_logs_filter = availablelogsfilter
        self.available_logs = availablelogs

        # setup class variables
        self.path_file_dict = dict()
        self.removed_logs_dict = dict()

        config = Config()
        available_filter = config.get_config("available_logs_filter")
        if(available_filter):
            self.available_logs_filter.insert(available_filter)

        selected_logs = config.get_config('selected_logs')

        for selected_log_item_key, selected_log_item_value in selected_logs.items():
            self.removed_logs_dict[selected_log_item_value['text']] = selected_log_item_value['statusTip']

        existing_log_locations = config.get_config("existing_log_locations")
        self.add_log_files(existing_log_locations)

        ava_log_style_str = config.array_config_str('available_logs_style')
        if ava_log_style_str:
            self.available_logs.setStyleSheet(ava_log_style_str)

        ava_log_filter_style_str = config.array_config_str('available_log_filter_style')
        if ava_log_filter_style_str:
            self.available_logs_filter.setStyleSheet(ava_log_filter_style_str)

    def add_log_files(self, loglocationslist):
        """ Expand all the log locations in the loglocationslist and add the files """
        self.path_file_dict.clear()
        for loglocation in loglocationslist:
            file_path_list = glob.glob(os.path.expanduser(loglocation))

            for full_file_and_path in file_path_list:
                log_file = ntpath.basename(full_file_and_path)
                self.path_file_dict[log_file] = full_file_and_path

            self.filter_available_logs()

    def filter_available_logs(self):
        """
        Filter the display of the available logs for the entered filter regex in
        available_logs_filter
        """
        text = self.available_logs_filter.text()
        str_regex = '.*' + text + '.*'

        self.available_logs.clear()

        if not text:
            for (log_file, log_location) in self.path_file_dict.items():
                if log_file not in self.removed_logs_dict:
                    self.available_logs.addItem(self.create_list_item(log_file,log_location))
        else:
            for (log_file, log_location) in self.path_file_dict.items():
                if re.match(str_regex, log_file) and log_file not in self.removed_logs_dict:
                    self.available_logs.addItem(self.create_list_item(log_file,log_location))

    def create_list_item(self,log_file,log_location):
        list_item = QListWidgetItem()
        list_item.setText(log_file)
        list_item.setStatusTip(log_location)

        return list_item

    def list_item_activated(self, listWidgetItem):
        """ Move activated item from the available logs list to the selected logs list """
        key = listWidgetItem.text()
        self.removed_logs_dict[key] = listWidgetItem.statusTip()
        self.available_logs.takeItem(self.available_logs.row(listWidgetItem))

    def unselect_log(self, log_name, log_location):
        if log_name in self.removed_logs_dict:
            del self.removed_logs_dict[log_name]
            self.filter_available_logs()
