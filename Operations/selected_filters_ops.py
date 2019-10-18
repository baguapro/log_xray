"""
Display the selected filters that are applied to the logs
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5.QtWidgets import QListWidgetItem

from Operations.config import Config

class SelectedFiltersOps():
    def __init__(self, selectedFilters):
        self.selected_filters = selectedFilters

        config = Config()
        selected_filters_style_str = config.array_config_str('selected_filters_style')
        if selected_filters_style_str:
            self.selected_filters.setStyleSheet(selected_filters_style_str)

    def add_new_filter(self, listWidgetItem):
        list_widget_item = listWidgetItem.clone()
        self.selected_filters.addItem(list_widget_item)
        self.selected_filters.setCurrentItem(list_widget_item)

    def remove_filter(self, listWidgetItem):
       self.selected_filters.takeItem(self.selected_filters.row(listWidgetItem))

    def refresh_selected_filter(self, listWidgetDict):
        """ Populate the selected filters list with the values in listWidgetDict """
        self.selected_filters.clear()
        for filter_name, filter_regex in listWidgetDict.items():
            list_item = self.create_list_item(filter_name, filter_regex)
            self.add_new_filter(list_item)

    def create_list_item(self,filter_name,filter_regex):
        list_item = QListWidgetItem()
        list_item.setText(filter_name)
        list_item.setStatusTip(filter_regex)

        return list_item
