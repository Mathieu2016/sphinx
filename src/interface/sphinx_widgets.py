from PyQt5.QtWidgets import QTextEdit


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)