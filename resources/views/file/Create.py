import core.facade as facade
import core.helpers as helpers

import database as db

from PyQt6.QtWidgets import(
    QGridLayout,
    
    QLineEdit,
    QComboBox,
    QLabel,
    QPushButton,
    
    QFileDialog
)

class File(facade.DialogWindow):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title = helpers.env('APP_NAME') + ' - Загрузка'
        self.setFixedSize(400, 150)
        
        # Области
        self.main_layout = QGridLayout()
        
        self.main_layout.addLayout(self.main_layout, 0, 0)
        
        #Виджеты
        self.setLayout(self.main_layout)
        
        self.file_label = QLabel()
        self.file_label.setText('Файл')
        self.main_layout.addWidget(self.file_label, 0, 0, 1, 2)
        
        self.file_path_label = QLineEdit()
        self.file_path_label.setPlaceholderText('Не выбрано')
        self.main_layout.addWidget(self.file_path_label, 1, 0)
        
        self.file_set_button = QPushButton()
        self.file_set_button.setText('Обзор...')
        self.file_set_button.clicked.connect(self.fileSelect)
        self.main_layout.addWidget(self.file_set_button, 1, 1)
        
        self.bank_select_label = QLabel()
        self.bank_select_label.setText('Банк')
        self.main_layout.addWidget(self.bank_select_label, 2, 0, 1, 2)
        
        self.bank_select = QComboBox()
        for bank in self.getBanks():
            self.bank_select.addItem(f'{bank.code} - {bank.name}', bank.code)
        self.main_layout.addWidget(self.bank_select, 3, 0, 1, 2)
        
        self.submit_button = QPushButton()
        self.submit_button.setText('Отправить')
        self.submit_button.clicked.connect(self.submit)
        self.main_layout.addWidget(self.submit_button, 4, 0, 1, 2)
        
    def getBanks(self):
        with db.session() as session:
            return session.query(db.models['glossary__banks']).all()
    
    def fileSelect(self):
        file_path = QFileDialog.getOpenFileName(self, None, None, 'CSV Files (*.csv)')[0]
        if file_path:
            self.file_path_label.setText(file_path)
    
    def submit(self):
        pass
            