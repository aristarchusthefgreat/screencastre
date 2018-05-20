from PyQt5.QtWidgets import QWidget, QBoxLayout, QTextEdit

from modules.read import ReadFile


class Help(QWidget):

    box: QBoxLayout

    read = None

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Help')
        self.setGeometry(350,350,450,600)
        self.setFixedSize(self.width(), self.height())
        self.box = QBoxLayout(QBoxLayout.RightToLeft, self)
        self.textEdit = QTextEdit(self)
        self.box.addWidget(self.textEdit)
        self.setLayout(self.box)

    def process(self, file):
        self.read = ReadFile(file)
        stream = self.read.open()
        self.textEdit.setText(stream.readAll())

