"""
Main entry point of the GUI application
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from GUIDesign.main_application import Ui_MainWindow
from GUIFunctional.log_location_dialog_functional import LogLocationDialogFunctional
from GUIFunctional.log_filter_dialog_functional import LogFilterDialogFunctional
from Operations.available_logs_ops import AvailableLogsOps
from Operations.events_dispatcher import EventsDispatcher
from Operations.named_method_dict import namedMethodDict
from Operations.global_information_ops import globalInformationOps
from Operations.selected_logs_ops import SelectedLogsOps
from Operations.display_logging_manager_ops import DisplayLoggingManagerOps
from Operations.open_logs_search_ops import OpenLogsSearchOps
from Operations.available_filter_ops import AvailableFilterOps
from Operations.selected_filters_ops import SelectedFiltersOps

#from PyQt5.QtGui import QColor

class MainWindowGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindowGUI, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ops = namedMethodDict()

        self.configure_widgets()
        self.configure_actions()
        self.setup_operations()

    """
    Configure the application title, and menu item tool tip
    """
    def configure_widgets(self):
        self.setWindowTitle('log xray')
        self.ui.actionAdd_Log_Directory.setStatusTip('Open Log Locations Dialog')
        self.ui.actionExit.setStatusTip('Exit log xray')

    """
    Configure the menu item keyboard shortcuts
    """
    def configure_actions(self):
        self.ui.actionExit.triggered.connect(self.exit_application)
        self.ui.actionExit.setShortcut('Ctrl+Q')

        self.ui.actionAdd_Log_Directory.triggered.connect(self.open_log_locations_dialog)
        self.ui.actionAdd_Log_Directory.setShortcut('Ctrl+L')

        self.ui.actionAdd_Log_Filter.triggered.connect(self.open_log_filter_dialog)
        self.ui.actionAdd_Log_Filter.setShortcut('Ctrl+F')

    """
    Initialise the applications functional components and events signal and slots
    """
    def setup_operations(self):
        self.logLocationDialog = LogLocationDialogFunctional()

        self.ops.available_logs_ops = AvailableLogsOps(
                self.ui.availableLogsFilter,
                self.ui.availableLogs
            )

        self.ops.global_information_ops = globalInformationOps(self.ui.globalInformation)
        self.ops.selected_logs_ops = SelectedLogsOps(self.ui.selectedLogsList)
        self.ops.display_logging_manager_ops = DisplayLoggingManagerOps(self.ui.logDisplayTabs)
        self.ops.open_logs_search_ops = OpenLogsSearchOps(self.ui.openLogsSearch, self.ops.global_information_ops)
        self.ops.available_filter_ops = AvailableFilterOps(self.ui.availableFilters, self.ui.availableFilterFilter)
        self.ops.selected_filters_ops = SelectedFiltersOps(self.ui.selectedFilters)

        self.ops.events_dispatcher = EventsDispatcher(self.ui, self.ops)
       
        self.log_filter_dialog = LogFilterDialogFunctional(self.ops.available_filter_ops)

    def exit_application(self):
        self.close()

    def open_log_locations_dialog(self):
        self.logLocationDialog.show_log_location_dialog(
                self.ops.available_logs_ops
            )

    def open_log_filter_dialog(self):
        self.log_filter_dialog.show_filter_location_dialog()

    """
    Catch the keyboard commands and forward on. 
    """
    def keyPressEvent(self, key_event):
        # At present the application is unable to catch keyboard events in the individual widgets
        # so all keyboard events have to be captured in the main application window and forwarded
        # on to the log processing manager
        if (key_event.modifiers() & Qt.AltModifier):
            if (key_event.key() == Qt.Key_G):
                self.ops.display_logging_manager_ops.goto_line_info()
                self.ops.open_logs_search_ops.init_goto_line()
            elif (key_event.key() == Qt.Key_S):
                self.ops.display_logging_manager_ops.search_info()
                self.ops.open_logs_search_ops.init_search_log()
            elif (key_event.key() == Qt.Key_N):
                self.ops.open_logs_search_ops.process_ops_input()
            elif (key_event.key() == Qt.Key_P):
                self.ops.open_logs_search_ops.process_search_prev()
            elif (key_event.key() == Qt.Key_R):
                self.ops.display_logging_manager_ops.refresh_log_data()
            elif (key_event.key() == Qt.Key_0):
                self.ops.open_logs_search_ops.run_selected(0)
            elif (key_event.key() == Qt.Key_1):
                self.ops.open_logs_search_ops.run_selected(1)
            elif (key_event.key() == Qt.Key_2):
                self.ops.open_logs_search_ops.run_selected(2)
            elif (key_event.key() == Qt.Key_3):
                self.ops.open_logs_search_ops.run_selected(3)
            elif (key_event.key() == Qt.Key_4):
                self.ops.open_logs_search_ops.run_selected(4)
            elif (key_event.key() == Qt.Key_5):
                self.ops.open_logs_search_ops.run_selected(5)
            elif (key_event.key() == Qt.Key_6):
                self.ops.open_logs_search_ops.run_selected(6)
            elif (key_event.key() == Qt.Key_7):
                self.ops.open_logs_search_ops.run_selected(7)
            elif (key_event.key() == Qt.Key_8):
                self.ops.open_logs_search_ops.run_selected(8)
            elif (key_event.key() == Qt.Key_9):
                self.ops.open_logs_search_ops.run_selected(9)

