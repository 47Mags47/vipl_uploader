from core.facade import Page
from core.helpers import env, user
import database as db

import uuid
import datetime

from resources.views.file.Create import File as File_create

from PyQt6.QtWidgets import(
    QGridLayout,
    
    QWidget,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    
    QAbstractScrollArea,
    
    QSizePolicy
)
from PyQt6.QtCore import Qt

class Event(Page):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title = env('APP_NAME') + ' - Выплата'
        
        self.min_width = 1200
        self.min_heidth = 800
        
        # Области
        self.main_layout = QGridLayout()
        self.top_layout = QGridLayout()
        self.table_layout = QGridLayout()
        
        self.main_layout.addLayout(self.top_layout, 0, 0)
        self.main_layout.addLayout(self.table_layout, 1, 0)
        
        #Виджеты
        self.container = QWidget()
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)
        
        self.back_button = QPushButton()
        self.back_button.setText('Назад')
        self.back_button.clicked.connect(lambda: self.goto('calendar'))
        self.top_layout.addWidget(self.back_button, 0, 0)
        
        self.add_button = QPushButton()
        self.add_button.setText('Добавить')
        self.add_button.clicked.connect(self.showCreateDialog)
        self.top_layout.addWidget(self.add_button, 0, 1)
        
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['UUID', 'Банк', 'Статус', 'Загружен', 'Дата загрузки', 'Записей', 'На сумму', 'Ошибок'])
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table_layout.addWidget(self.table)

        # Размеры
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)

    def getData(self, event):
        current_user = user()
        with db.session() as session:
            # Получаем или создаем пакет
            package_m = db.models['main__packages']
            package_query = session.query(package_m)\
                .filter(package_m.division_code==current_user.division_code)\
                .filter(package_m.event_id==event.id)
            if(package_query.count() == 0):
                package = package_m()
                package.id = uuid.uuid4()
                package.status_code = 'created'
                package.division_code = current_user.division_code
                package.event_id = event.id
                package.created_at = datetime.datetime.now().isoformat()
                package.updated_at = datetime.datetime.now().isoformat()
                session.add(package)
            self.package = package_query.first() 
            
            # Ищем файлы пакета
            file_m = db.models['main__package__files']
            bank_m = db.models['glossary__banks']
            status_m = db.models['glossary__package__file_statuses']
            user_m = db.models['main__users']
            
            files = session.query(file_m, bank_m, status_m, user_m)\
                .filter(file_m.package_id==self.package.id)\
                .join(bank_m, file_m.bank_code == bank_m.code)\
                .join(status_m, file_m.status_code == status_m.code)\
                .join(user_m, file_m.upload_user_id == user_m.id)
        
        # Очищаем таблицу
        while (self.table.rowCount() > 0):
            self.table.removeRow(0)
        
        # Выводим новый список
        for i, (file, bank, status, uploaded) in enumerate(files.all()):
            self.table.insertRow(i)
            
            uuid_item = QTableWidgetItem()
            uuid_item.setText(f'{file.id}')
            self.table.setItem(i, 0, uuid_item)
            
            bank_item = QTableWidgetItem()
            bank_item.setText(f'{bank.code} - {bank.name}')
            self.table.setItem(i, 1, bank_item)
            
            status_item = QTableWidgetItem()
            status_item.setText(f'{status.name}')
            self.table.setItem(i, 2, status_item)
            
            user_item = QTableWidgetItem()
            user_item.setText(f'{current_user.FIO}')
            self.table.setItem(i, 3, user_item)
            
            created_at_item = QTableWidgetItem()
            created_at_item.setText(f'{file.created_at.strftime('%d.%m.%Y %H:%I')}')
            self.table.setItem(i, 4, created_at_item)
    def showCreateDialog(self):
        dialog = File_create()
        dialog.exec()
        