from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMainWindow
import sys



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Post')
        self.resize(600,400)
        self.style
















app = QtWidgets.QApplication(sys.argv)
app.exec()
