from core.facade import Page
from core.helpers import env
import database as db

from pandas import date_range
from datetime import date, timedelta

from PyQt6.QtWidgets import(
    QGridLayout,
    QFormLayout,
    
    QWidget,
    QLabel,
    QCalendarWidget,
    QListWidget,
    QListWidgetItem,
    QPushButton,
)
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt

class Calendar(Page):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title = env('APP_NAME') + ' - Календарь'
        
        self.min_width = 1200
        self.min_heidth = 800
        
        # Области
        self.main_layout = QGridLayout()
        self.event_list_layout = QFormLayout()
        
        # Виджеты
        self.container.setLayout(self.main_layout)
        
        self.calendar = QCalendarWidget()
        self.main_layout.addWidget(self.calendar, 0, 0)
        
        self.event_list_box = QWidget()
        self.event_list_box.setLayout(self.event_list_layout)
        self.main_layout.addWidget(self.event_list_box, 0, 1)
        
        self.event_list_label = QLabel()
        self.event_list_label.setText('Список выплат')
        self.event_list_layout.addRow(self.event_list_label)
        
        self.event_list = QListWidget()
        self.event_list_layout.addRow(self.event_list)
        
        self.getEventList()
        
        # События
        self.calendar.currentPageChanged.connect(self.getEventList)
    
    def getEventList(self, year = date.today().year, month = date.today().month):
        self.event_list.clear()
        
        # Получение дат
        startOfMount = date(year, month, 1)
        next_mount =  startOfMount.replace(day=28) + timedelta(days=4)
        endOfMount = next_mount - timedelta(next_mount.day)
        
        startOfperiod = startOfMount - timedelta(days=startOfMount.weekday())
        endOfPeriod = endOfMount + timedelta(days=(7 - endOfMount.isoweekday()))
        
        # Получение списка событий по дням
        date_list = date_range(startOfperiod, endOfPeriod).to_pydatetime().tolist()
        
        with db.session() as session:
            events = session.query(db.models['main__calendar__events'])\
                .filter(db.models['main__calendar__events'].date.between(startOfperiod.strftime('%Y-%m-%d'), endOfPeriod.strftime('%Y-%m-%d')))\
                .all()
        
        event_for_day_list = {}
        for day in date_list:
            event_for_day_list[day.strftime('%d.%m.%Y')] = []
        
        for event in events:
            event_for_day_list[event.date.strftime('%d.%m.%Y')].append(event)
        
        # Заполнение списка
        for date_str, events in event_for_day_list.items():
            date_layout = QFormLayout()
            
            date_box = QWidget()
            date_box.setLayout(date_layout)
            
            date_label = QLabel()
            date_label.setText(f'{date_str}')
            date_layout.addRow(date_label)
            
            date_list_layout = QFormLayout()
            
            date_list_box = QWidget()
            date_list_box.setStyleSheet(''' QWidget{border: 1px solid black} ''')
            date_list_box.setLayout(date_list_layout)
            date_layout.addRow(date_list_box)
            
            for event in events:
                event_link = QPushButton()
                event_link.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                event_link.setText(f'{event.description}')
                if event.status_code != 'opened':
                    event_link.setEnabled(False)
                event_link.clicked.connect(lambda clicked, data = event: self.goto('event', data))
                style = '''
                    QPushButton{
                        text-align: left;
                        border:none;
                    }
                    QPushButton:hover{
                        text-decoration: underline;
                    }
                '''
                event_link.setStyleSheet(style)
                
                date_list_layout.addRow(event_link)
            
            item = QListWidgetItem(self.event_list)
            self.event_list.insertItem(self.event_list.count(), item)
            self.event_list.setItemWidget(item, date_box)
            item.setSizeHint(date_layout.sizeHint())