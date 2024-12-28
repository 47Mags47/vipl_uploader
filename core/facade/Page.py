from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import pyqtSignal

class Page(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.container = QWidget()
        self.setCentralWidget(self.container)
    
    gotoSignal = pyqtSignal(str, object, name='gotoSignal')
    def goto(self, page, data = {}):
        self.gotoSignal.emit(page, data)