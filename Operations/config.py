"""
Singleton class that reads and writes the applications working data in json format
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


import json

class Config():
    """
    Inner class of Config only one instance should exist in the application
    """
    class __config_inner():
        def __init__(self ):
            self.json_config_data = None
            self.config_location = None

        def load_config(self, configLocation):
            """ Load json data at configLocation """
            self.config_location = configLocation
            with open(configLocation) as json_config_file:
                self.json_config_data = json.load(json_config_file)

        def save_config_data(self):
            with open(self.config_location, 'w') as json_file:
                json.dump(self.json_config_data, json_file, indent=4)

    instance = __config_inner()

    def load_config(self, configLocation):
        self.instance.load_config(configLocation)

    def get_config(self, config):
        if config in self.instance.json_config_data:
            return self.instance.json_config_data[config]

        return dict()

    def array_config_str(self, config):
        """ return the config data in config as a string """
        config_str = ""
        if config in self.instance.json_config_data:
            for data in self.instance.json_config_data[config]:
                config_str = config_str + data + "; "

        return config_str

    def add_config_data(self, name, value):
        self.instance.json_config_data[name] = value

    def remove_config_data(self, name):
        if name in self.instance.json_config_data:
            del self.instance.json_config_data[name]

    def save_config_data(self):
        self.instance.save_config_data()
