#!venv/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from modules import *
from windows import *
from _constants import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drpdwn_driver = QComboBox(self)
        self.lbl_frmrt = QLabel(self)
        self.lbl_driver = QLabel(self)
        self.lbl_drpdwn_audio = QLabel(self)
        self.lbl_miscellany_head = QLabel(self)
        self.rec_section_head = QLabel(self)
        self.drpdwn_frmrt = QComboBox(self)
        self.drpdwn_audioSelect = QComboBox(self)
        self.record = QPushButton('', self)
        self.stop = QPushButton('', self)
        self.btn_playback = QPushButton('', self)
        self.txtFileLoc = QLineEdit(self)

        self.video = None

        self.audio = audio.Audio()
        self.widget = QWidget(self)

        self.menubar = QMenuBar()
        self.file = QMenu('File')
        self.help = QMenu('Help')
        self.settings = QAction('Global Settings...')
        self.exit = QAction('Quit', self)
        self.open_new_pnt_window = QAction('Open New Whiteboard', self)
        self.resume_whiteboarding = QAction('Resume Whiteboarding', self)
        self.open_help = QAction('Getting Started', self)

        self.setStyleSheet(
            'background-color:white;'

        )

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.v_record_stop = QVBoxLayout()
        self.h_record_stop = QHBoxLayout()
        self.v_miscellany = QVBoxLayout()
        self.h_miscellany = QHBoxLayout()
        self.h_lbl_drpdwn_audio = QHBoxLayout()
        self.h_lbl_drpdwn_driver = QHBoxLayout()
        self.h_lbl_drpdwn_frmrt = QHBoxLayout()

        self.initUI()
        self.w = paintWindow.NewScene()
        self.f1 = help.Help()
        self.change_settings = settings.Window()

    def initUI(self):

        self.topMenu()

        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(ASSETS_DIR, 'red-record-512.png')))
        self.record.setFixedSize(40, 40)
        self.record.setIcon(icon)
        self.record.setIconSize(QSize(32, 32))
        self.record.setToolTip('Record the Screen')
        self.record.resize(self.record.sizeHint())
        self.record.setStyleSheet('background-color:white;')

        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(ASSETS_DIR, 'stop.png')))
        self.stop.setFixedSize(40, 40)
        self.stop.setIcon(icon)
        self.stop.setIconSize(QSize(32, 32))
        self.stop.setToolTip('Stop Recording')
        self.stop.resize(self.stop.sizeHint())
        self.stop.setEnabled(False)
        self.stop.setStyleSheet('background-color:white;')

        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(ASSETS_DIR, 'play.jpeg')))
        self.btn_playback.setIcon(icon)
        self.btn_playback.setIconSize(QSize(32, 32))
        self.btn_playback.setToolTip('Playback video...')
        self.btn_playback.resize(self.btn_playback.sizeHint())
        self.btn_playback.setEnabled(False)
        self.btn_playback.setFixedSize(40, 40)

        regex = QRegExp("[a-zA-Z0-9_]+")
        validator = QRegExpValidator(regex)
        self.txtFileLoc.resize(280, 40)
        self.txtFileLoc.setFixedHeight(40)
        self.txtFileLoc.setMinimumWidth(100)
        self.txtFileLoc.setValidator(validator)

        self.drpdwn_audioSelect.addItem('default')
        self.drpdwn_audioSelect.addItems(self.audio.AVAILABLE_DEVICES)
        self.drpdwn_audioSelect.setMaximumWidth(300)

        self.drpdwn_frmrt.addItems(FRAMERATES)
        self.drpdwn_frmrt.setMaximumWidth(200)

        self.record.clicked.connect(self.startRecording)
        self.stop.clicked.connect(self.stopRecording)
        self.btn_playback.clicked.connect(self.playback)

        self.rec_section_head.setText('Record the Screen')
        self.rec_section_head.setStyleSheet('font-weight: bold; color: #00164A; font-family: sans-serif;')

        self.lbl_miscellany_head.setText('Settings')
        self.lbl_miscellany_head.setStyleSheet('font-weight: bold; color: #00164A; font-family: sans-serif;')

        self.lbl_drpdwn_audio.setText('Audio Input')
        self.lbl_drpdwn_audio.setStyleSheet('font-weight: bold; color: #6A5A6A; font-family: sans-serif;')

        self.lbl_driver.setText('Audio Driver')
        self.lbl_driver.setStyleSheet('font-weight: bold; color: #6A5A6A; font-family: sans-serif;')

        self.lbl_frmrt.setText('Framerate')
        self.lbl_frmrt.setStyleSheet('font-weight: bold; color: #6A5A6A; font-family: sans-serif;')

        self.drpdwn_driver.addItem('Alsa')
        self.drpdwn_driver.addItem('Pulse')
        self.setMaximumWidth(100)

        self.statusBar()

        self.setWindowTitle("Screencaster 1.0")
        self.center()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)

        self.h_record_stop.setDirection(QBoxLayout.RightToLeft)
        self.v_record_stop.setDirection(QBoxLayout.BottomToTop)
        self.h_miscellany.setDirection(QBoxLayout.RightToLeft)
        self.h_lbl_drpdwn_audio.setDirection(QBoxLayout.RightToLeft)
        self.h_lbl_drpdwn_driver.setDirection(QBoxLayout.RightToLeft)
        self.h_lbl_drpdwn_frmrt.setDirection(QBoxLayout.RightToLeft)
        self.v_miscellany.setDirection(QBoxLayout.BottomToTop)
        self.h_record_stop.addStretch(1)
        self.v_record_stop.addStretch(1)
        self.h_miscellany.addStretch(1)
        self.v_miscellany.addStretch(1)
        self.h_lbl_drpdwn_audio.addStretch(1)
        self.h_lbl_drpdwn_driver.addStretch(1)
        self.h_lbl_drpdwn_frmrt.addStretch(1)

        self.h_record_stop.addWidget(self.btn_playback)
        self.h_record_stop.addWidget(self.stop)
        self.h_record_stop.addWidget(self.record)
        self.v_record_stop.addLayout(self.h_record_stop)

        self.h_lbl_drpdwn_audio.addWidget(self.drpdwn_audioSelect)
        self.h_lbl_drpdwn_audio.addWidget(self.lbl_drpdwn_audio)
        self.h_lbl_drpdwn_driver.addWidget(self.drpdwn_driver)
        self.h_lbl_drpdwn_driver.addWidget(self.lbl_driver)
        self.h_lbl_drpdwn_frmrt.addWidget(self.drpdwn_frmrt)
        self.h_lbl_drpdwn_frmrt.addWidget(self.lbl_frmrt)
        self.v_miscellany.addLayout(self.h_lbl_drpdwn_audio)
        self.v_miscellany.addLayout(self.h_miscellany)
        self.v_miscellany.addLayout(self.h_lbl_drpdwn_driver)
        self.v_miscellany.addLayout(self.h_lbl_drpdwn_frmrt)

        self.grid.addWidget(self.rec_section_head, 0, 0, 1, 2)
        self.grid.addWidget(line, 1, 0, 1, 2)
        self.grid.addWidget(self.txtFileLoc, 2, 0, 1, 2)
        self.grid.addLayout(self.v_record_stop, 3, 0)
        self.grid.addWidget(self.lbl_miscellany_head, 4, 0, 1, 2)
        self.grid.addWidget(line1, 5, 0, 1, 2)
        self.grid.addLayout(self.v_miscellany, 6, 0, 1, 1)
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)

        self.w = paintWindow.NewScene()

    def topMenu(self):
        self.menubar.setStyleSheet('background-color:#E2E2E2;')

        self.settings.setShortcut('Ctrl+Shift+S')
        self.settings.triggered.connect(lambda: self.preferences())

        self.exit.setShortcut('Ctrl+Q')
        self.exit.triggered.connect(lambda: sys.exit(0))

        self.open_new_pnt_window.setShortcut('Ctrl+N')
        self.open_new_pnt_window.triggered.connect(lambda: self.paint())

        self.resume_whiteboarding.setShortcut('Ctrl+C')
        self.resume_whiteboarding.triggered.connect(lambda: self.paint(False))
        self.resume_whiteboarding.setEnabled(False)

        self.open_help.setShortcut('F1')
        self.open_help.triggered.connect(lambda : self.view_help())

        self.file.addAction(self.open_new_pnt_window)
        self.file.addAction(self.resume_whiteboarding)
        self.file.addSeparator()
        self.file.addAction(self.settings)
        self.file.addAction(self.exit)

        self.help.addAction(self.open_help)

        self.menubar.addMenu(self.file)
        self.menubar.addMenu(self.help)

        self.setMenuBar(self.menubar)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startRecording(self):

        os.environ["File"] = self.txtFileLoc.text()

        if SETTINGS.settings_list['av'] == 'True':
            av_audio = True
        else:
            av_audio = False

        self.video = ffmpeg.AV_COMPILE(av_audio, self.drpdwn_driver.currentText(), self.drpdwn_audioSelect.currentText(),
                                       self.drpdwn_frmrt.currentText())

        self.video.start()

        if self.video.isRunning:
            self.statusBar().showMessage('Recording...')
            self.stop.setEnabled(True)
            self.record.setEnabled(False)
            self.btn_playback.setEnabled(False)

    def stopRecording(self):
        if self.video.isRunning:
            self.video.stop()

        if not self.video.isRunning:
            self.statusBar().showMessage('Saving...')
            self.video.compile()

            self.statusBar().showMessage('Stopped')
            self.stop.setEnabled(False)
            self.record.setEnabled(True)
            self.btn_playback.setEnabled(True)

    def playback(self):
        try:
            vlc.Play(os.environ['LastFile'])
        except KeyError as e:
            dialog.ErrorMsg(repr(e))

    def paint(self, clear=True):

        if clear:
            self.w.scene.clear()

        self.w.show()
        self.resume_whiteboarding.setEnabled(True)

    def view_help(self):
        self.f1.process('getting_started.txt')
        self.f1.show()

    def exit(self):
        sys.exit(0)

    def preferences(self):
        self.change_settings.show()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            sys.exit(0)
        elif e.key() == Qt.Key_R:
            self.startRecording()
        elif e.key() == Qt.Key_C:
            self.stopRecording()
        elif e.key() == Qt.Key_P:
            self.paint()

    def closeEvent(self, e):
        if self.video is not None:
            if self.video.isRunning:
                from modules import dialog
                dlg = dialog.QuestionDialog('You are currently recording. Do you wish to quit? If so, your data may be lost.')
                if dlg.clickedButton() == dlg.yes:
                    e.accept()
                else:
                    e.ignore()
            else:
                e.accept()
        else:
            e.accept()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    splash_img = QPixmap('splash.jpg')
    splash = QSplashScreen(splash_img, Qt.WindowStaysOnTopHint)
    splash.showMessage('Loading data...')
    splash.show()

    w = MainWindow()

    splash.finish(w)

    w.show()

    screen_resolution = app.desktop().screenGeometry()
    os.environ['Width'], os.environ['Height'] = str(screen_resolution.width()), str(screen_resolution.height())

    sys.exit(app.exec_())
