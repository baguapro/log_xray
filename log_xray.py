"""
Main application entry point.
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5 import QtWidgets

from GUIFunctional.main_window import MainWindowGUI
from Operations.config import Config

if __name__ == "__main__":
    import sys, getopt

    configurations = Config()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:',['configfile='])

        if not opts:
            print(sys.argv[0], '-c /json/config/file/location')
            sys.exit(2)

    except getopt.GetoptError:
        print(sys.argv[0], '-c /json/config/file/location')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0], '-c /json/config/file/location')
            sys.exit()
        elif opt in ('-c','--configfile'):
            configurations.load_config(arg)

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindowGUI()
    MainWindow.show()
    sys.exit(app.exec_())
