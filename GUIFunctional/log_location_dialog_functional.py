"""
Dialog that enables the entering of log directory locations, regex's can be used 
for the log directories
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'

import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from GUIDesign.log_location_dialog import Ui_logLocations
from Operations.config import Config

class LogLocationDialogFunctional():
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_logLocations()
        self.ui.setupUi(self.dialog)

        config = Config()
        existing_log_locations = config.get_config("existing_log_locations")

        for log_location in existing_log_locations:
            self.ui.existingLogLocation.addItem(log_location)

        self.configure_locations_dialog()
        self.configure_locations_actions()

    def configure_locations_dialog(self):
        """ Configure dialog menu tip """
        self.ui.logLocationAdd.setStatusTip('Add Log File Location')

    def configure_locations_actions(self):
        """ Configure the dialog keyboard shortcuts """
        self.ui.logLocationExit.clicked.connect(self.exit_dialog)
        self.ui.logLocationExit.setShortcut('Ctrl+Q')

        self.ui.logLocationAdd.clicked.connect(self.add_location)
        self.ui.logLocationAdd.setShortcut('Ctrl+N')

        self.ui.logLocationRemove.clicked.connect(self.remove_selected_location)
        self.ui.logLocationRemove.setShortcut('Ctrl+R')

    def exit_dialog(self):
        """
        On exit of the dialog, save the changes and forward directory locations to
        the available logs handler
        """
        self.dialog.close()
        locations_list = self.get_locations_list()
        config = Config()
        config.add_config_data("existing_log_locations", locations_list)
        config.save_config_data()

        self.available_logs_ops.add_log_files(locations_list)

    def add_location(self):
        log_location = self.ui.enterLogLocation.text()
        log_location.strip()

        if log_location:
            self.ui.existingLogLocation.addItem(log_location)

    def remove_selected_location(self):
        selected_items = self.ui.existingLogLocation.selectedItems()

        if selected_items:
            for item in selected_items:
                self.ui.existingLogLocation.takeItem(
                    self.ui.existingLogLocation.row(item)
                    )

    def show_log_location_dialog(self, availablelogsops):
        self.available_logs_ops = availablelogsops
        self.dialog.show()

    def get_locations_list(self):
        """ return the entered locations as a standard python list """
        all_items = [str(self.ui.existingLogLocation.item(i).text()) 
                        for i in range(self.ui.existingLogLocation.count())]
        return all_items
