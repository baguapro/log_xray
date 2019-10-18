"""
Single place to register all signals and slots helping to avoid cupling 
between GUI elements and function providing objects
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from Operations.config import Config

class EventsDispatcher():
    def __init__(self, uiElements, operations):
        self.ui_elements = uiElements
        self.operations = operations

        uiElements.availableLogsFilter.textEdited.connect(operations.available_logs_ops.filter_available_logs)
        uiElements.availableLogsFilter.editingFinished.connect(self.save_available_logs_filter_config)
        uiElements.availableLogs.itemSelectionChanged.connect(self.available_logs_selection_changed)
        uiElements.availableLogs.itemActivated.connect(operations.selected_logs_ops.add_new_log)
        uiElements.availableLogs.itemActivated.connect(operations.available_logs_ops.list_item_activated)
        operations.selected_logs_ops.add_selected_log.connect(operations.display_logging_manager_ops.open_logging_process)

        # selected logs signal / slots
        operations.selected_logs_ops.itemSelectionChanged.connect(self.selected_logs_selection_changed)
        uiElements.openLogsSearch.editingFinished.connect(operations.open_logs_search_ops.process_ops_input)
        operations.open_logs_search_ops.goto_line.connect(operations.display_logging_manager_ops.process_goto_line)
        operations.open_logs_search_ops.search.connect(operations.display_logging_manager_ops.process_search_str)
        operations.display_logging_manager_ops.goto_line_history_data.connect(operations.open_logs_search_ops.process_goto_history_data)
        operations.display_logging_manager_ops.search_history_data.connect(operations.open_logs_search_ops.process_search_history_data)
        operations.open_logs_search_ops.search_prev.connect(operations.display_logging_manager_ops.process_search_prev)
        operations.display_logging_manager_ops.selected_tab_changed.connect(operations.selected_logs_ops.update_active_item)

        # log filter events
        uiElements.availableFilterFilter.textEdited.connect(operations.available_filter_ops.filter_available_filters)
        uiElements.availableFilterFilter.editingFinished.connect(operations.available_filter_ops.save_filter_filter)
        uiElements.availableFilters.itemSelectionChanged.connect(self.available_filter_selection_changed)
        uiElements.availableFilters.itemActivated.connect(operations.display_logging_manager_ops.add_filter_to_log)
        uiElements.availableFilters.itemActivated.connect(operations.selected_filters_ops.add_new_filter)
        uiElements.availableFilters.itemActivated.connect(operations.available_filter_ops.list_item_activated)

        uiElements.selectedFilters.itemActivated.connect(operations.display_logging_manager_ops.remove_filter_from_log)
        uiElements.selectedFilters.itemActivated.connect(operations.available_filter_ops.filter_available)
        uiElements.selectedFilters.itemActivated.connect(operations.selected_filters_ops.remove_filter)

        uiElements.logDisplayTabs.currentChanged.connect(operations.display_logging_manager_ops.tab_changed)
        operations.display_logging_manager_ops.filters_on_tab.connect(operations.available_filter_ops.log_tab_filter_update)
        operations.display_logging_manager_ops.filters_on_tab.connect(operations.selected_filters_ops.refresh_selected_filter)

        uiElements.logDisplayTabs.tabCloseRequested.connect(operations.display_logging_manager_ops.close_tab)
        operations.display_logging_manager_ops.log_tab_closed.connect(operations.selected_logs_ops.remove_log)
        operations.display_logging_manager_ops.log_tab_closed.connect(operations.available_logs_ops.unselect_log)
        
        operations.selected_logs_ops.fire_selected_signal()
        operations.display_logging_manager_ops.signal_init_tab_details()

    # process the displaying of global information here to save every GUI element from
    # needing a reference to the global information widget
    def available_logs_selection_changed(self):
        selected_items = self.ui_elements.availableLogs.selectedItems()
        if selected_items:
            self.operations.global_information_ops.display_info(selected_items[0].statusTip())

    def available_filter_selection_changed(self):
        selected_items = self.ui_elements.availableFilters.selectedItems()
        if selected_items:
            self.operations.global_information_ops.display_info(selected_items[0].statusTip())

    def save_available_logs_filter_config(self):
        text = self.ui_elements.availableLogsFilter.text()
        config = Config()
        config.add_config_data("available_logs_filter",text)
        config.save_config_data()

    def selected_logs_selection_changed(self):
        selected_items = self.operations.selected_logs_ops.selectedItems()
        if selected_items:
            self.operations.global_information_ops.display_info(selected_items[0].statusTip())
            self.operations.display_logging_manager_ops.switch_tabs(selected_items[0])

