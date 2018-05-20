from modules import dialog
from PyQt5.Qt import QKeySequence, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QFileDialog
from PyQt5.QtWidgets import QWidget, QShortcut
from _constants import *


class Window(QWidget):

    ext_list = [
        'mkv',
        'mp4',
        'avi'
    ]

    def __init__(self):
        QWidget.__init__(self)

        self.v_box = QVBoxLayout()
        self.v_dir = QVBoxLayout()
        self.v_ext = QVBoxLayout()
        self.v_av = QVBoxLayout()
        self.H_default_save_dir = QHBoxLayout()
        self.H_default_ext = QHBoxLayout()
        self.H_av = QHBoxLayout()
        self.H_save = QHBoxLayout()

        self.settings = xml.ParseXMLSettings()

        self.txt_default_dir = QLineEdit(self)
        self.drpdwn_av = QComboBox(self)
        self.drpdwn_ext = QComboBox(self)

        self.shortcut = QShortcut(
            QKeySequence('Ctrl+W'), self)
        self.shortcut.activated.connect(self.close)

        self.initUI()

        self.v_box.addSpacing(12)
        self.H_av.addSpacing(12)
        self.H_default_ext.addSpacing(12)
        self.H_default_save_dir.addSpacing(12)
        self.H_save.addSpacing(12)

        self.setLayout(self.v_box)

        self.setGeometry(200, 200, 250, 150)
        self.setWindowTitle('Global Settings')

    def initUI(self):

        self.txt_default_dir.setText(self.settings.settings_list['save_dir'])
        self.txt_default_dir.setEnabled(False)
        lbl_default_dir = QLabel(self)
        lbl_default_dir.setText('Default Directory: ')
        btn_default_dir = QPushButton(self)
        btn_default_dir.setText('Change...')

        self.drpdwn_av.addItem(self.settings.settings_list['av'])
        lbl_av = QLabel(self)
        lbl_av.setText('Record Audio and Video? ')

        self.drpdwn_ext.addItem(self.settings.settings_list['ext'])
        lbl_ext = QLabel(self)
        lbl_ext.setText('Video Extension: ')

        btn_save = QPushButton(self)
        btn_save.setText('Save changes...')

        btn_default_dir.clicked.connect(lambda: self.change_dir())
        btn_save.clicked.connect(self.save)

        if self.settings.settings_list['av'] == 'True':
            self.drpdwn_av.addItem('False')
        else:
            self.drpdwn_av.addItem('True')

        for ext in self.ext_list:
            if ext != self.settings.settings_list['ext']:
                self.drpdwn_ext.addItem(ext)

        self.v_dir.addWidget(lbl_default_dir)
        self.H_default_save_dir.addWidget(self.txt_default_dir)
        self.H_default_save_dir.addWidget(btn_default_dir)
        self.v_dir.addLayout(self.H_default_save_dir)
        self.v_av.addWidget(lbl_av)
        self.H_av.addWidget(self.drpdwn_av)
        self.v_av.addLayout(self.H_av)
        self.v_ext.addWidget(lbl_ext)
        self.H_default_ext.addWidget(self.drpdwn_ext)
        self.v_ext.addLayout(self.H_default_ext)
        self.H_save.addWidget(btn_save)

        self.v_ext.addStretch(1)
        self.v_av.addStretch(1)
        self.v_dir.addStretch(1)

        self.v_box.addLayout(self.v_dir)
        self.v_box.addLayout(self.v_av)
        self.v_box.addLayout(self.v_ext)
        self.v_box.addLayout(self.H_save)

        self.v_box.addStretch(1)

    def save(self):
        if self.drpdwn_ext.currentText() != self.settings.settings_list['ext'] or self.drpdwn_av.currentText() != self.settings.settings_list['av']:
            dlg = dialog.QuestionDialog('Are you ready to save changes?')
            if dlg.clickedButton() == dlg.yes:
                if self.drpdwn_ext.currentText() != self.settings.settings_list['ext']:
                    self.settings.edit('ext', self.drpdwn_ext.currentText())
                    SETTINGS.settings_list['ext'] = self.drpdwn_ext.currentText()
                if self.drpdwn_av.currentText() != self.settings.settings_list['av']:
                    self.settings.edit('av', self.drpdwn_av.currentText())
                    SETTINGS.settings_list['av'] = self.drpdwn_av.currentText()
        else:
            pass

    def change_dir(self):
        dlg = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if dlg != "":
            self.settings.edit('save_dir', dlg)
            self.txt_default_dir.setText(dlg)
            SETTINGS.settings_list['save_dir'] = dlg



