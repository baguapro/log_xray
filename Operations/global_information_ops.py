"""
Single place to register all signals and slots helping to avoid cupling 
between GUI elements and function providing objects
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from Operations.config import Config

class globalInformationOps():
    def __init__(self, globalInformation):
        self.global_information = globalInformation

        config = Config()
        style_str = config.array_config_str('global_information_style')
        if style_str:
            self.global_information.setStyleSheet(style_str);

    def clear(self):
        self.global_information.selectAll()
        self.global_information.backspace()

    def display_info(self, info):
        self.clear()
        self.global_information.insert(info)
