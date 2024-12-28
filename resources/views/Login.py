from core.facade import Page
from core.helpers import env, pickle
import database as db

from PyQt6.QtWidgets import( 
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt

import bcrypt

class Login(Page):
    def __init__(self):
        super().__init__()
        
        # Настройка окна
        self.title = env('APP_NAME') + ' - Вход'
        
        self.min_width = 300
        self.max_width = 300
        self.min_heidth = 150
        self.max_heidth = 150
        
        # Виджеты
        label_header = QLabel('Вход')
        label_header.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.error_label = QLabel()
        self.error_label.setStyleSheet('color: red')
        
        email_label = QLabel('Email')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('example@mail.ru')
        
        password_label = QLabel('Пароль')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('******')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_button = QPushButton('Отправить')
        login_button.clicked.connect(self.login)
        
        # Разметка
        layout = QFormLayout()
        layout.addRow(label_header)
        layout.addRow(self.error_label)
        layout.addRow(email_label, self.email_input)
        layout.addRow(password_label, self.password_input)
        layout.addRow(login_button)
        
        self.container.setLayout(layout)
        
    # Слоты
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key.Key_Return:
            self.login()
            
    # Сигналы
    
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
 
        with db.session() as session:
            query = session.query(db.models['main__users']).filter_by(email=email)
            if (query.count() > 0):
                user = query.one()
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    pickle.write('user_id', user.id)
                    self.goto('calendar')
                else:
                    self.auth_error()
                    return False
            else:
                self.auth_error()
                return False
            
    def auth_error(self):
        self.error_label.setText('* Неверный логин или пароль')
        