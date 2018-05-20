from PyQt5.QtCore import QFile, QTextStream, QIODevice


class ReadFile:

    def __init__(self, file):
        self.file = QFile(file)

    def open(self) -> object:
        self.file.open(QIODevice.ReadOnly)
        return QTextStream(self.file)
