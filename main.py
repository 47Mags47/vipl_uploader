from core.facade import MainWindow
from core.helpers import user

from PyQt6.QtWidgets import QApplication

import sys
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.goto('calendar' if user() != None else 'login')
    window.show()
    app.exec()
    