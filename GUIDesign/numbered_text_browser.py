"""
Modified code taken from source ...
provides a text display object with line number column
"""

__version__ = '0.01'
__author__ = 'Adrian Phung'


from PyQt5.Qt import QFrame, QWidget, QTextBrowser, QHBoxLayout, QPainter, QMargins, QPalette

from Operations.config import Config

class NumberedTextBrowser(QFrame):

    class NumberBar(QWidget):

        def __init__(self, *args):
            QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = '0'
            self.orig_line_number = []

        def reset_data(self):
            self.orig_line_number.clear()
            self.highest_line = '0'
            self.edit.clear()

        def setOriginalLineNum(self,line_number):
            self.orig_line_number.append(str(line_number))

        def setLineNumberList(self, line_numbers):
            self.orig_line_number = line_numbers

        def setTextEdit(self, edit):
            self.edit = edit

        def update(self, *args):
            '''
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            '''
            # The + 4 is used to compensate for the current line being bold.
            width = self.fontMetrics().width(self.highest_line) + 4
            if self.width() != width:
                self.setFixedWidth(width)
            QWidget.update(self, *args)

        def paintEvent(self, event):
            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())

            painter = QPainter(self)

            line_count = 0
            line_count_str = ''
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                orig_number = ''
                line_count += 1

                if len(self.orig_line_number) >= line_count:
                    orig_number = self.orig_line_number[line_count -1]

                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break

                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)

                if orig_number:
                    line_count_str = str(line_count) + ' | ' + str(orig_number)
                else:
                    line_count_str = str(line_count)

                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(self.width() - font_metrics.width(line_count_str) - 3, round(position.y()) - contents_y + font_metrics.ascent(), line_count_str)

                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                block = block.next()

            self.highest_line = line_count_str
            painter.end()

            QWidget.paintEvent(self, event)


    def __init__(self, *args):
        QFrame.__init__(self, *args)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        self.edit = QTextBrowser()
        self.edit.setFrameStyle(QFrame.NoFrame)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)

        hbox = QHBoxLayout(self)
        hbox.setSpacing(0)
        margins = QMargins(0,0,0,0)
        hbox.setContentsMargins(margins)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)

        config = Config()
        style_str = config.array_config_str('log_line_number_style')

        self.setStyleSheet(style_str)

    def refresh_data(self, new_data):
        self.number_bar.reset_data()
        line_number_list = new_data['line_number'].tolist()
        self.number_bar.setLineNumberList(line_number_list)
        lines = new_data['log_line'].tolist()

        for line in lines:
            self.edit.append(line)

    def reset_data(self):
        self.number_bar.reset_data()

    def setOriginalLineNum(self,line_number):
        self.number_bar.setOriginalLineNum(line_number)

    def eventFilter(self, object, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if object in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return QFrame.eventFilter(object, event)

    def getTextEdit(self):
        return self.edit
