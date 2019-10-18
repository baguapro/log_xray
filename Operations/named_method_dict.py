"""
Provide a more elegent interface to get / set the dict name = value
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


class namedMethodDict(dict):
    """
    overload dict to give dict.value access instead of dict['value']
    by overloading __getattr__ and setattr__
    """

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        # set any attributes here - before initialisation
        # these remain as normal attributes
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True
        # after initialisation, setting attributes is the same as setting an item

    def __getattr__(self, item):
        """
        Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values.
        Only if we are initialised
        """
        if '_namedMethodDict__initialised' not in self.__dict__:  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif item not in self.__dict__:       # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)
