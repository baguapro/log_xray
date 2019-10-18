"""
Displays a list of the log filters entered into the Create Log Filters Dialog
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


import re

from PyQt5.QtWidgets import QListWidgetItem

from Operations.config import Config

class AvailableFilterOps():
    def __init__(self, availableFilters, availableFiltersFilter):
        self.available_filters = availableFilters
        self.available_filters_filter = availableFiltersFilter

        self.filters_dict = dict()
        self.removed_filters_dict = dict()

        config = Config()
        available_filter = config.get_config("available_filters_filter")
        if(available_filter):
            self.available_filters_filter.insert(available_filter)

        existing_filters = config.get_config('existing_filters')

        for existing_filters_key, existing_filters_value in existing_filters.items():
            self.filters_dict[existing_filters_value['text']] = existing_filters_value['statusTip']

        self.filter_available_filters()

        ava_filters_style_str = config.array_config_str('available_filters_style')
        if ava_filters_style_str:
            self.available_filters.setStyleSheet(ava_filters_style_str)

        ava_filters_filter_style_str = config.array_config_str('available_filters_filter_style')
        if ava_filters_filter_style_str:
            self.available_filters_filter.setStyleSheet(ava_filters_filter_style_str)

    def add_log_filters(self, logFiltersList):
        """
        All all the filters in logFiltersList (which is the list entered into the 
        create log filters dialog)
        """
        self.filters_dict.clear()

        for row in range(logFiltersList.count()):
            add_row = logFiltersList.item(row).clone()
            self.filters_dict[add_row.text()] = add_row.statusTip()

        self.filter_available_filters()

    def filter_available_filters(self):
        """ Filter the available filters based on the entered regex """
        text = self.available_filters_filter.text()
        str_regex = '.*' + text + '.*'

        self.available_filters.clear()

        if not text:
            for (filter_name, filter_regex) in self.filters_dict.items():
                if filter_name not in self.removed_filters_dict:
                    self.available_filters.addItem(self.create_new_item(filter_name, filter_regex))
        else:
            for (filter_name, filter_regex) in self.filters_dict.items():
                if re.match(str_regex, filter_name) and filter_name not in self.removed_filters_dict:
                    self.available_filters.addItem(self.create_new_item(filter_name, filter_regex))

    def create_new_item(self,display_name,filter_regex):
        list_item = QListWidgetItem()
        list_item.setText(display_name)
        list_item.setStatusTip(filter_regex)

        return list_item

    def list_item_activated(self, listWidgetItem):
        """ Move the filter in the listWidgetItem to the selected filters list """
        key = listWidgetItem.text()
        self.removed_filters_dict[key] = listWidgetItem.statusTip()
        self.available_filters.takeItem(self.available_filters.row(listWidgetItem))

    def save_filter_filter(self):
        text = self.available_filters_filter.text()
        config = Config()
        config.add_config_data("available_filters_filter",text)
        config.save_config_data()

    def log_tab_filter_update(self, log_filters_dict):
        """
        log_filters_dict are the filers in the selected filters list so
        they should not be displayed in the available filters list
        """
        self.removed_filters_dict = log_filters_dict.copy()
        self.filter_available_filters()

    def filter_available(self, listWidgetItem):
        """
        The filter in listWidgetItem should be added back into the available
        filters list
        """
        if listWidgetItem.text() in self.removed_filters_dict:
            del self.removed_filters_dict[listWidgetItem.text()]
            self.filter_available_filters()

