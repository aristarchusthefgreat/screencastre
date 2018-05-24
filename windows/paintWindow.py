import traceback
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from _constants import *
from modules import dialog, common


class NewScene(QOpenGLWidget):

    saved = False
    tmp_lst = list()
    redo_lst = list()
    deleted_lines = list()

    def __init__(self):
        QWidget.__init__(self)

        self.mouseLoc = None
        self.lastPos = None

        self.line_colour = None
        self.thickness = None
        self.pen = None
        self.brush = None

        self.lastPos = None

        self.__drawing = False
        self.__menuOpen = False
        self.__undo_depth = -1

        self.setCursor(Qt.CrossCursor)
        self.setGeometry(1200, 1200, 1400, 800)
        self.setWindowTitle("Whiteboard 0.1 Beta")
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.box = QBoxLayout(QBoxLayout.LeftToRight, self)
        self.box.addWidget(self.view)
        self.setLayout(self.box)

        self.scene.setSceneRect(0, 0, self.width(), self.height())
        self.ellipses = list()
        self.lines = list()

        self.shortcut = QShortcut(
            QKeySequence('Ctrl+W'), self)
        self.shortcut.activated.connect(self.close)
        self.undoDrawing = QShortcut(
            QKeySequence('Ctrl+Z'), self)
        self.undoDrawing.activated.connect(self.undo)
        self.new = QShortcut(
            QKeySequence('Ctrl+Shift+N'), self
        )
        self.redoDrawing = QShortcut(
            QKeySequence('Ctrl+Y'), self
        )
        self.redoDrawing.activated.connect(self.redo)
        self.new.activated.connect(self.clearGraphic)

        self.initUI()
        self.initTools()
        self.center()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.scene.mousePressEvent = self.mouseDown
        self.scene.mouseReleaseEvent = self.mouseUp
        self.scene.mouseMoveEvent = self.mouseMove
        self.scene.contextMenuEvent = self.contextMenu

    def initTools(self, colour=Qt.black, thickness=6):
        self.line_colour = colour
        self.thickness = thickness
        self.pen = QPen(self.line_colour, self.thickness)
        self.brush = QBrush(self.line_colour)

    def mouseDown(self, e):
        if self.__undo_depth > -1:
            self.__undo_depth = -1

        if self.__drawing == False and e.button() == Qt.LeftButton:
            if self.__menuOpen:
                self.__menuOpen = False

            if not self.__menuOpen:
                self.__drawing = True
        if e.button() == Qt.RightButton:
            self.__menuOpen = True
        if not self.__menuOpen:
            self.lastPos = common.Point(e.scenePos().x(), e.scenePos().y())
            self.tmp_lst.append([])
            self.tmp_lst[-1].append(self.scene.addLine(QLineF(QPoint(self.lastPos.X, self.lastPos.Y), QPoint(self.lastPos.X, self.lastPos.Y)), self.pen))
            self.lines.append({
                'Line': {
                    'Points': {
                        'begin': [self.lastPos.X, self.lastPos.Y],
                        'end': [self.lastPos.X, self.lastPos.Y]
                    },
                    'Thickness': self.thickness,
                    'Colour': self.line_colour,
                }
            })
            self.saved = False

    def mouseUp(self, e):
        if self.__drawing:
            self.__drawing = False
            self.mouseLoc = None

    def mouseMove(self, e):
        if self.__drawing:
            if self.mouseLoc is not None:
                self.lastPos = self.mouseLoc
            self.mouseLoc = common.Point(e.scenePos().x(), e.scenePos().y())
            self.tmp_lst[-1].append(self.scene.addLine(QLineF(QPoint(self.lastPos.X, self.lastPos.Y), QPoint(self.mouseLoc.X, self.mouseLoc.Y)), self.pen))
            self.lines.append({
                'Line': {
                    'Points': {
                        'begin': [self.lastPos.X, self.lastPos.Y],
                        'end': [self.mouseLoc.X, self.mouseLoc.Y]
                    },
                    'Thickness': self.thickness,
                    'Colour': self.line_colour,
                }
            })

    def contextMenu(self, e):
        self.menu = QMenu(self)
        self.line_thickness = QMenu('Line Thickness', self.menu)
        yellow = QAction(QIcon(ASSETS_DIR + '/' + 'yellow.png'), 'Yellow', self)
        yellow.triggered.connect(lambda: self.initTools(Qt.yellow, self.thickness))
        green = QAction(QIcon(ASSETS_DIR + '/' + 'green.png'), 'Green', self)
        green.triggered.connect(lambda: self.initTools(Qt.green, self.thickness))
        red = QAction(QIcon(ASSETS_DIR + '/' + 'red.png'), 'Red', self)
        red.triggered.connect(lambda: self.initTools(Qt.red, self.thickness))
        blue = QAction(QIcon(ASSETS_DIR + '/' + 'blue.png'), 'Blue', self)
        blue.triggered.connect(lambda: self.initTools(Qt.blue, self.thickness))
        cyan = QAction(QIcon(ASSETS_DIR + '/' + 'cyan.png'), 'Cyan', self)
        cyan.triggered.connect(lambda: self.initTools(Qt.cyan, self.thickness))
        magenta = QAction(QIcon(ASSETS_DIR + '/' + 'magenta.png'), 'Magenta', self)
        magenta.triggered.connect(lambda: self.initTools(Qt.magenta, self.thickness))
        gray = QAction(QIcon(ASSETS_DIR + '/' + 'gray.png'), 'Gray', self)
        gray.triggered.connect(lambda: self.initTools(Qt.gray, self.thickness))
        black = QAction(QIcon(ASSETS_DIR + '/' + 'black.png'), 'Black', self)
        black.triggered.connect(lambda: self.initTools(Qt.black, self.thickness))
        erase = QAction(QIcon(ASSETS_DIR + '/' + 'eraser.png'), 'Eraser', self)
        erase.triggered.connect(lambda: self.initTools(Qt.white, 50))
        normal = QAction(QIcon(ASSETS_DIR + '/' + 'pen.png'), 'Normal', self)
        normal.triggered.connect(lambda: self.initTools(Qt.black))
        new = QAction(QIcon(ASSETS_DIR + '/' + 'new.png'), 'New', self)
        new.triggered.connect(lambda: self.clearGraphic())
        save = QAction(QIcon(ASSETS_DIR + '/' + 'save.png'), 'Save', self)
        save.triggered.connect(lambda: self.saveGraphic())
        load = QAction(QIcon(ASSETS_DIR + '/' + 'load.png'), 'Load', self)
        load.triggered.connect(lambda: self.openGraphic())
        default = QAction(QIcon(ASSETS_DIR + '/' + '6p-line.png'), 'default', self)
        default.triggered.connect(lambda: self.initTools(self.line_colour))
        thick_2 = QAction(QIcon(ASSETS_DIR + '/' + '2p-line.png'), '2px', self)
        thick_2.triggered.connect(lambda: self.initTools(self.line_colour, 2))
        thick_4 = QAction(QIcon(ASSETS_DIR + '/' + '4p-line.png'), '4px', self)
        thick_4.triggered.connect(lambda: self.initTools(self.line_colour, 4))
        thick_8 = QAction(QIcon(ASSETS_DIR + '/' + '6p-line.png'), '8px', self)
        thick_8.triggered.connect(lambda: self.initTools(self.line_colour, 8))
        thick_10 = QAction(QIcon(ASSETS_DIR + '/' + '10p-line.png'), '10px', self)
        thick_10.triggered.connect(lambda: self.initTools(self.line_colour, 10))
        thick_12 = QAction(QIcon(ASSETS_DIR + '/' + '12p-line.png'), '12px', self)
        thick_12.triggered.connect(lambda: self.initTools(self.line_colour, 12))
        self.menu.addSection('Options')
        self.menu.addAction(new)
        self.menu.addAction(load)
        self.menu.addAction(save)
        self.menu.addSection('Colours')
        self.menu.addAction(yellow)
        self.menu.addAction(green)
        self.menu.addAction(red)
        self.menu.addAction(blue)
        self.menu.addAction(cyan)
        self.menu.addAction(magenta)
        self.menu.addAction(gray)
        self.menu.addAction(black)
        self.menu.addSection('Pens')
        self.menu.addAction(erase)
        self.menu.addAction(normal)
        self.menu.addSeparator()
        self.line_thickness.addAction(default)
        self.line_thickness.addSeparator()
        self.line_thickness.addAction(thick_2)
        self.line_thickness.addAction(thick_4)
        self.line_thickness.addAction(thick_8)
        self.line_thickness.addAction(thick_10)
        self.line_thickness.addAction(thick_12)
        self.menu.addMenu(self.line_thickness)
        self.menu.popup(QCursor.pos())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_S:
            self.saveGraphic()
        if e.key() == Qt.Key_O:
            self.openGraphic()
        if e.key() == Qt.Key_P:
            self.saveScreen()

    def saveGraphic(self):
        saveFile = dialog.SaveDialog('new-save.scr', '*.scr')
        try:
            if saveFile.fname[0] != '':
                common.Save(saveFile.fname[0], self.lines)
                self.saved = True
        except:
            e = traceback.format_exc()
            dialog.ErrorMsg(e)

    def openGraphic(self):

        openFile = dialog.OpenDialog()

        if openFile.filenames:
            new_file = openFile.filenames[0]
        else:
            new_file = None

        if new_file != '' and new_file is not None:
            try:
                self.clearGraphic()
                data = common.Open(new_file)

                for line in data.Contents:

                    if line['Line']['Colour'] == 2:
                        line['Line']['Colour'] = Qt.black
                    elif line['Line']['Colour'] == 12:
                        line['Line']['Colour'] = Qt.yellow
                    elif line['Line']['Colour'] == 8:
                        line['Line']['Colour'] = Qt.green
                    elif line['Line']['Colour'] == 7:
                        line['Line']['Colour'] = Qt.red
                    elif line['Line']['Colour'] == 9:
                        line['Line']['Colour'] = Qt.blue
                    elif line['Line']['Colour'] == 5:
                        line['Line']['Colour'] = Qt.gray

                    self.initTools(line['Line']['Colour'], line['Line']['Thickness'])

                    self.scene.addLine(QLineF(QPoint(line['Line']['Points']['begin'][0], line['Line']['Points']['begin'][1]),
                                              QPoint(line['Line']['Points']['end'][0], line['Line']['Points']['end'][1])),
                                       self.pen)

                    self.lines.append({
                        'Line': {
                            'Points': {
                                'begin': [
                                    line['Line']['Points']['begin'][0],
                                    line['Line']['Points']['begin'][1]
                                ],
                                'end': [
                                    line['Line']['Points']['end'][0],
                                    line['Line']['Points']['end'][1]
                                ]
                            },
                            'Thickness': line['Line']['Thickness'],
                            'Colour': line['Line']['Colour'],
                        }
                    })
                    self.tmp_lst = list()
                    self.deleted_lines = list()
                    self.redo_lst = list()
            except:
                e = traceback.format_exc()
                dialog.ErrorMsg(e)

    def clearGraphic(self):

        if not self.saved:
            svdlg = dialog.QuestionDialog('You have unsaved changes, are you sure you wish to start again?')
            if svdlg.clickedButton() == svdlg.yes:
                self.scene.clear()
                self.ellipses = list()
            else:
                pass
        else:
            self.scene.clear()
            self.ellipses = list()

    def saveScreen(self):

        try:
            saveFile = dialog.SaveDialog('new-save.jpg')

            if saveFile.fname[0] != '':
                screen = self.grab()
                screen.save(saveFile.fname[0], 'jpg')
        except:
            e = traceback.format_exc()
            dialog.ErrorMsg(e)

    def undo(self):
        if self.tmp_lst:
            self.redo_lst.append([])
            for line in self.tmp_lst[-1]:
                self.redo_lst[-1].append(line)
                line.setVisible(False)
                self.deleted_lines.append(self.lines[-1])
                self.lines.pop()
            self.tmp_lst.pop()

    def redo(self):
        if self.redo_lst:
            self.tmp_lst.append([])
            for line in self.redo_lst[-1]:
                line.setVisible(True)
                self.tmp_lst[-1].append(line)
                self.lines.append(self.deleted_lines[-1])
                del self.deleted_lines[-1]
            del self.redo_lst[-1]

    def closeEvent(self, e):
        if not self.saved:
            svdlg = dialog.QuestionDialog('You have unsaved changes, are you sure you wish to quit?')
            if svdlg.clickedButton() == svdlg.yes:
                e.accept()
            else:
                e.ignore()
        else:
            e.accept()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    ex = NewScene()
    ex.show()
    sys.exit(app.exec_())
