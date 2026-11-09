from src.csv_utils import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget,
)
import sys

USE = "csv" # csv | sqlite

with open('src/style.css', 'r') as f:
    STYLE = f.read()

class MainWindow(QMainWindow):
    def __init__(self, csv: bool, title, subtitle, fields, button_text, switch_text, link_text):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
 
        title_label = QLabel(title)
        title_label.setObjectName("title")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("subtitle")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(18)
        
        # fields: list of (key, label, placeholder, is_password)
        self.inputs = {}
        self.password_inputs = []
        for key, label, placeholder, is_password in fields:
            field_label = QLabel(label.upper())
            field_label.setObjectName("fieldLabel")
            edit = QLineEdit()
            edit.setPlaceholderText(placeholder)
            if is_password:
                edit.setEchoMode(QLineEdit.EchoMode.Password)
                self.password_inputs.append(edit)
            self.inputs[key] = edit
            layout.addWidget(field_label)
            layout.addWidget(edit)
            layout.addSpacing(8)
 
        # Show/hide password
        self.show_password = QCheckBox("Show password")
        self.show_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.show_password.toggled.connect(self._toggle_password)
        layout.addWidget(self.show_password)
        layout.addSpacing(14)
 
        # Submit button
        self.submit_button = QPushButton(button_text)
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.submit_button)
        layout.addSpacing(10)
 
        # "Don't have an account? Register"
        switch_row = QHBoxLayout()
        switch_row.addStretch()
        switch_row.addWidget(QLabel(switch_text))
        self.switch_button = QPushButton(link_text)
        self.switch_button.setObjectName("linkButton")
        self.switch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        switch_row.addWidget(self.switch_button)
        switch_row.addStretch()
        layout.addLayout(switch_row)
 
    def _toggle_password(self, visible):
        mode = QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        for edit in self.password_inputs:
            edit.setEchoMode(mode)

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.resize(520, 700)
        self.setMinimumSize(440, 640)
 
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
 
        # Pages
        self.login_page = FormPage(
            "Welcome back", "Sign in to continue",
            [
                ("username", "Username", "Enter your username", False),
                ("password", "Password", "Enter your password", True),
            ],
            "Sign in", "Don't have an account?", "Register",
        )
        self.register_page = FormPage(
            "Create account", "Fill in the details to get started",
            [
                ("username", "Username", "Choose a username", False),
                ("password", "Password", "Choose a password", True),
                ("confirm", "Confirm password", "Repeat your password", True),
            ],
            "Register", "Already have an account?", "Sign in",
        )
 
        self.stack = QStackedWidget()
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
 
        # Card
        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(380)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.addWidget(self.stack)
 
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 160))
        card.setGraphicsEffect(shadow)
 
        # Center the card in the window
        root_layout = QVBoxLayout(root)
        root_layout.addStretch()
        root_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        root_layout.addStretch()
 
        # Switching between forms
        self.login_page.switch_button.clicked.connect(lambda: self.show_page(1))
        self.register_page.switch_button.clicked.connect(lambda: self.show_page(0))
 
        # Hook your own logic here:
        self.login_page.submit_button.clicked.connect(self.on_login)
        self.register_page.submit_button.clicked.connect(self.on_register)
 
        self.show_page(0)
 
    def show_page(self, index):
        # Only the visible page counts for sizing, so the card fits each form
        for i in range(self.stack.count()):
            policy = QSizePolicy.Policy.Preferred if i == index else QSizePolicy.Policy.Ignored
            self.stack.widget(i).setSizePolicy(policy, policy)
        self.stack.setCurrentIndex(index)
        self.stack.updateGeometry()
 
    def on_login(self):
        username = self.login_page.inputs["username"].text()
        password = self.login_page.inputs["password"].text()
        # TODO: call your login function here
 
    def on_register(self):
        username = self.register_page.inputs["username"].text()
        password = self.register_page.inputs["password"].text()
        confirm = self.register_page.inputs["confirm"].text()
        # TODO: call your register function here

if __name__ == '__main__':
    csv = USE == "csv"
    if csv:
        header_type: list[type] = [str, float, str, int, str]
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])
        catalogue = Database()
        catalogue.SAVE_FILE()
    else:
        header_type: list[type] = [str, float, str, int, str]  # Changer pour utiliser du CSV
        CREATE_FILE(header=['product', 'price', 'description', 'stock', 'quality'])  # Changer pour utiliser du CSV
        catalogue = Database()  # Changer pour utiliser du CSV
        catalogue.SAVE_FILE() # Changer pour utiliser du CSV
        
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())