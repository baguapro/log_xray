"""
Ddisplays the logs selected for action.
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5.QtWidgets import QListWidgetItem, QListWidget
from PyQt5 import QtCore

from Operations.config import Config

class SelectedLogsOps(QListWidget):
    
    add_selected_log = QtCore.pyqtSignal(QListWidgetItem)

    def __init__(self, selectedLogsList):
        QListWidget.__init__(self, selectedLogsList)

        self.selected_logs = dict()

        config = Config()
        self.selected_logs = config.get_config('selected_logs')

        for selected_log_item_key, selected_log_item_value in self.selected_logs.items():
            list_item = self.create_list_widget_item(selected_log_item_value['text'],
                                                     selected_log_item_value['statusTip'])
            self.add_new_log(list_item,False)

        selected_logs_style = config.array_config_str('selected_logs_style')
        if selected_logs_style:
            self.setStyleSheet(selected_logs_style)

    def add_new_log(self, listWidgetItem, saveConfig=True):
        list_widget_item = listWidgetItem.clone()
        if saveConfig:
            selected_log_item = dict()
            selected_log_item['text'] = list_widget_item.text()
            selected_log_item['statusTip'] = list_widget_item.statusTip()
            self.selected_logs['selected_log_item_' + str(len(self.selected_logs))] = selected_log_item
            config = Config()
            config.add_config_data("selected_logs",self.selected_logs)
            config.save_config_data()

        self.addItem(list_widget_item)
        self.setCurrentItem(list_widget_item)
        self.add_selected_log.emit(list_widget_item)

    def remove_log(self, log_name, log_location):
        config_name = self.get_config_name_for_log(log_name)
        if config_name:
            del self.selected_logs[config_name]

        for count in range(self.count()):
            list_item = self.item(count)
            if list_item.text()==log_name and list_item.statusTip()==log_location:
                self.takeItem(count)
                break

        config = Config()
        config.add_config_data("selected_logs",self.selected_logs)
        config.save_config_data()

    def fire_selected_signal(self):
        """
        Used at application startup after configs have been read to signal list
        of selected logs read from config. (log display widget catches the signal
        and opens the logs applying saved configurations)
        """
        for count in range(self.count()):
            list_widget_item = self.item(count)
            self.add_selected_log.emit(list_widget_item)

    def create_list_widget_item(self, name, location):
        list_item = QListWidgetItem()
        list_item.setText(name)
        list_item.setStatusTip(location)

        return list_item

    def get_config_name_for_log(self, log_name):
        """ Get the name of the configuration the log details are saved under """
        for config_name, config_value in self.selected_logs.items():
            if log_name == config_value['text']:
                return config_name

        return None

    def update_active_item(self, name):
        """ make the list item named 'name' the current selected item """
        list_items = self.findItems(name, QtCore.Qt.MatchExactly)
        if list_items:
            self.setCurrentItem(list_items[0])
