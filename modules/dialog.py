from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QDir


class ErrorMsg(QMessageBox):
    __msg = None

    def __init__(self, msg):
        QMessageBox.__init__(self)

        self.setIcon(self.Warning)
        self.setStandardButtons(self.Ok)
        self.setWindowTitle('There has been as error!')
    
        self.__msg = msg
        self.setText(self.__msg)
        self.exec_()


class OpenDialog(QFileDialog):
    filenames = []

    def __init__(self,  suffix="*.scr", ext="Screencaster Files (*.scr)"):
        QFileDialog.__init__(self)
        self.FileMode(self.AnyFile)
        self.setNameFilter(ext)
        self.setDefaultSuffix(suffix)
        self.setDirectory(QDir.homePath() + '/Documents/')

        if (self.exec_()):
            self.filenames = self.selectedFiles()

    def __str__(self):
        return self.filenames[0]


class SaveDialog(QFileDialog):
    def __init__(self, default='', extension='*.jpg'):
        QFileDialog.__init__(self)
        self.fname = self.getSaveFileName(self, '', QDir.homePath() + "/" + default, extension)

    def __str__(self):
        return self.fname[0]


class QuestionDialog(QMessageBox):

    def __init__(self, msg):
        QMessageBox.__init__(self)
        self.setWindowTitle('Just checking...')
        self.no = self.addButton('No', QMessageBox.NoRole)
        self.yes = self.addButton('Yes', QMessageBox.YesRole)
        self.setIcon(self.Question)
        self.setText(msg)
        self.exec_()