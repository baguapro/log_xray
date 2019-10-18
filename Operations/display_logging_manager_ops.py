"""
Manager that controls the creation of tabs displaying the selected logs along with the 
objects that provides the functionality to query the logs for information.
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5 import QtWidgets, QtCore

from numbered_text_browser import NumberedTextBrowser
from Operations.display_log_processing_ops import DisplayLogProcessingOps

class DisplayLoggingManagerOps(QtWidgets.QTabWidget):

    goto_line_history_data = QtCore.pyqtSignal(list) 
    search_history_data = QtCore.pyqtSignal(list)
    filters_on_tab = QtCore.pyqtSignal(dict)
    log_tab_closed = QtCore.pyqtSignal(str, str)
    selected_tab_changed = QtCore.pyqtSignal(str)

    def __init__(self, logDisplayTabs):
        QtWidgets.QTabWidget.__init__(self, logDisplayTabs)

        self.log_display_tabs = logDisplayTabs
        self.log_display_tabs.setTabsClosable(True)
        self.display_log_processing_ops_dict = dict()
        self.name_widget_dict = dict()

    def open_logging_process(self, listWidgetItem):
        """ return the config data in config as a string """
        log_location = listWidgetItem.statusTip()
        log_name = listWidgetItem.text()

        # create the logging tab
        logging_tab = QtWidgets.QWidget()
        
        self.gridLayout = QtWidgets.QGridLayout(logging_tab)
        self.gridLayout.setObjectName("gridLayout_" + log_name)
        self.gridLayout.setContentsMargins(0,0,0,0)
        log_text_display = NumberedTextBrowser(logging_tab)
        self.gridLayout.addWidget(log_text_display, 0, 0, 1, 1)

        self.log_display_tabs.addTab(logging_tab,log_name)
       
        # save the logging details to out dict and start the log processing
        display_log_processing_ops = DisplayLogProcessingOps(log_location, log_text_display)
        display_log_processing_ops.start()
        self.display_log_processing_ops_dict[log_name] = display_log_processing_ops
        self.name_widget_dict[log_name] = logging_tab

    def close_tab(self, index):
        tab_name = self.log_display_tabs.tabText(index)
        if tab_name and tab_name in self.display_log_processing_ops_dict:
            location = self.display_log_processing_ops_dict[tab_name].get_logfile_location()
            self.display_log_processing_ops_dict[tab_name].stop_processing()
            del self.display_log_processing_ops_dict[tab_name]
            del self.name_widget_dict[tab_name]
            self.log_display_tabs.removeTab(index)
            self.log_tab_closed.emit(tab_name, location)

    def get_current_tab_name(self):
        return self.log_display_tabs.tabText(
                self.log_display_tabs.currentIndex()
            );

    def switch_tabs(self, listWidgetItem):
        """ switch the active to the tab named in listWidgetItem.text() """
        for i in range(self.log_display_tabs.count()):
            if(listWidgetItem.text()==self.log_display_tabs.tabText(i)):
                self.log_display_tabs.setCurrentWidget(self.log_display_tabs.widget(i))
    #
    # Log processing functionality, all follow the same pattern
    # 1. find the current active tab
    # 2. pass the requested functionality down to the log processing object linked to the tab
    #
    def process_goto_line(self, line_number):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].goto_line(line_number)

    def process_search_str(self, search_str):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].search(search_str)

    def process_search_prev(self, search_str):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].search_prev(search_str)

    def goto_line_info(self):
        current_tab = self.get_current_tab_name()
        if current_tab:
            prev_data = self.display_log_processing_ops_dict[current_tab].goto_line_info()
            self.goto_line_history_data.emit(prev_data)

    def search_info(self):
        current_tab = self.get_current_tab_name()
        if current_tab:
            prev_data = self.display_log_processing_ops_dict[current_tab].search_info()
            self.search_history_data.emit(prev_data)

    def add_filter_to_log(self, filterItem):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].add_filter(filterItem)

    def remove_filter_from_log(self, filterItem):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].remove_filter(filterItem)

    def refresh_log_data(self):
        current_tab = self.get_current_tab_name()
        if current_tab:
            self.display_log_processing_ops_dict[current_tab].refresh_data()

    # when a tab is changed ie. the active tab is switched, the filters that are applied
    # the new active tab need to be displayed. This method signals what filters should be
    # displayed.
    def tab_changed(self, index):
        tab_name = self.log_display_tabs.tabText(index)
        if tab_name and tab_name in self.display_log_processing_ops_dict:
            log_filters = self.display_log_processing_ops_dict[tab_name].tab_filters()
            self.filters_on_tab.emit(log_filters)
            self.selected_tab_changed.emit(tab_name)

    def signal_init_tab_details(self):
        current_tab = self.get_current_tab_name()
        if current_tab:
            log_filters = self.display_log_processing_ops_dict[current_tab].tab_filters()
            self.filters_on_tab.emit(log_filters)
