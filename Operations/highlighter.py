"""
Performs text colour highlighting based on provided regex and hex colour codes
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor

from Operations.config import Config

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)

        self.searchFormat = QTextCharFormat()
        self.searchFormat.setForeground(Qt.darkYellow)

        self.highlightingRules = []

        config = Config()
        highlight_config = config.get_config('log_highlighter')
        if highlight_config:
            for hl_config in highlight_config:
                text_format = QTextCharFormat()
                text_format.setForeground(QColor(hl_config['color']))
                self.highlightingRules.append((QRegExp(hl_config['regex']),text_format))

    def add_search_highlight(self, word):
        """
        Add word to the list of which will be highlighted based on the searchFormat
        highlighting
        """
        rule = (QRegExp(word), self.searchFormat)
        if rule not in self.highlightingRules:
            self.highlightingRules.append(rule)
            self.rehighlight()

    def highlightBlock(self, text):
        """
        Loop over the highlightingRules and apply the highlight colour code
        to the text if it matches the highlght regex
        """
        for pattern, format in self.highlightingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
