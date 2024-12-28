from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtCore import pyqtSlot, QSize
from typing import Any

from core.helpers import env
from core.facade.Page import Page

import resources.views as views

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Данные
        self.m_pages = {}
        
        # Настройки окна
        self.setWindowTitle(env('APP_NAME'))
        
        # Виджеты
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Считывание страниц
        self.initPages()
    
    def initPages(self):
        self.registerPage(views.Login(), "login")
        self.registerPage(views.Calendar(), "calendar")
        self.registerPage(views.Event(), "event")
        
    def registerPage(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, Page):
            widget.gotoSignal.connect(self.goto)
        
    @pyqtSlot(str, Any)
    def goto(self, name, data = {}):
        print(f'goto {name}, данные:\n{data}')
        widget = self.m_pages[name]
        
        title = widget.title if hasattr(widget, 'title') else env('APP_NAME')
        self.setWindowTitle(title)
        
        min_width =     widget.min_width    if hasattr(widget, 'min_width')     else 300
        max_width =     widget.max_width    if hasattr(widget, 'max_width')     else 1920
        min_heidth =    widget.min_heidth   if hasattr(widget, 'min_heidth')    else 200
        max_heidth =    widget.max_heidth   if hasattr(widget, 'max_heidth')    else 1680
        
        self.setMinimumSize(QSize(min_width, min_heidth))
        self.setMaximumSize(QSize(max_width, max_heidth))
        
        if hasattr(widget, 'getData') and callable(widget.getData):
            widget.getData(data)
        
        self.stacked_widget.setCurrentWidget(widget)