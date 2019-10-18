"""
Class providing the functional code for the Dialog that enables the entering of log filtering regex's 
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from GUIDesign.log_filter_dialog import Ui_logFilters

from Operations.config import Config

class LogFilterDialogFunctional():
    def __init__(self, appliedFilters):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_logFilters()
        self.ui.setupUi(self.dialog)

        self.applied_filters = appliedFilters

        self.selected_items = []

        config = Config()
        existing_filters = config.get_config('existing_filters')

        for filter_item_key, filter_item_value in existing_filters.items():
            list_item = self.create_new_item(filter_item_value['text'],filter_item_value['statusTip'])
            self.ui.existingFilters.addItem(list_item)

        self.configure_filters_dialog()
        self.configure_filters_actions()

    
    def configure_filters_dialog(self):
        """ configure dialog menu tip """
        self.ui.filterAdd.setStatusTip('Add Log Filter')

    def configure_filters_actions(self):
        """ configure the dialog keyboard shortcuts """
        self.ui.filterExit.clicked.connect(self.exit_dialog)
        self.ui.filterExit.setShortcut('Ctrl+Q')

        self.ui.filterAdd.clicked.connect(self.add_filter)
        self.ui.filterAdd.setShortcut('Ctrl+N')

        self.ui.filterRemove.clicked.connect(self.remove_selected_filter)
        self.ui.filterRemove.setShortcut('Ctrl+R')

        self.ui.existingFilters.itemSelectionChanged.connect(self.display_selected_item)

    def exit_dialog(self):
        """
        On exit of the dialog, save the changes and forward filtering regex's to
        the available handler
        """
        self.dialog.close()

        existing_filters = dict()

        for count in range(self.ui.existingFilters.count()):
            list_widget_item = self.ui.existingFilters.item(count)
       
            existing_filter_item = dict()
            existing_filter_item['text'] = list_widget_item.text()
            existing_filter_item['statusTip'] = list_widget_item.statusTip()
            existing_filters['existing_filter_' + str(count)] = existing_filter_item

        config = Config()
        config.add_config_data("existing_filters",existing_filters)
        config.save_config_data()

        self.applied_filters.add_log_filters(self.ui.existingFilters)

    def add_filter(self):
        """  Add the entered filtered details to the existingFilters list """
        display_name = self.ui.filterDisplayName.text()
        filter_regex = self.ui.filterRegexData.text()

        display_name.strip()
        filter_regex.strip()

        # only add the filter if values are entered
        if (display_name and filter_regex):
            new_item = self.create_new_item(display_name, filter_regex)

            # if there is an existing filter with the same name then
            # replace with the new filter
            existing_item = self.find_existing_selected(display_name)
            if existing_item:
                self.ui.existingFilters.takeItem(
                    self.ui.existingFilters.row(existing_item)
                    )

            self.ui.existingFilters.addItem(new_item)

    def create_new_item(self,display_name,filter_regex):
        list_item = QListWidgetItem()
        list_item.setText(display_name)
        list_item.setStatusTip(filter_regex)

        return list_item

    def find_existing_selected(self, display_name):
        if self.selected_items:
            for item in self.selected_items:
                if item.text()==display_name:
                    return item

        return None

    def remove_selected_filter(self):
        if self.selected_items:
            for item in self.selected_items:
                self.ui.existingFilters.takeItem(
                    self.ui.existingFilters.row(item)
                    )

    def display_selected_item(self):
        """ Display the selected existing filter item in the filter editing fields """
        self.selected_items = self.ui.existingFilters.selectedItems()
        if self.selected_items:
            item = self.selected_items[0]
            self.ui.filterDisplayName.clear()
            self.ui.filterRegexData.clear()

            self.ui.filterDisplayName.setText(item.text())
            self.ui.filterRegexData.setText(item.statusTip())

    def show_filter_location_dialog(self):
        self.dialog.show()
