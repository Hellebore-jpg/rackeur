from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget,
)

from dataclasses import dataclass

from ..utils.helpers import make_header

@dataclass(frozen=True)
class FieldSpec:
    key: str
    label: str
    placeholder: str
    is_password: bool = False
 
class FormPage(QWidget):
    """Fenêtre de connexion ou d'inscription avec nom d'utilisateur et mot de passe.
    """
 
    def __init__(self, title: str, subtitle: str, fields: list[FieldSpec], button_text: str, switch_text: str, link_text: str) -> None:
        """Initialise une fenêtre de connexion ou d'inscription avec les éléments spécifiés.

        Args:
            title (str): Titre de la fenêtre.
            subtitle (str): Sous-titre de la fenêtre.
            fields (list[FieldSpec]): Inputs à utiliser.
            button_text (str): Texte du bouton de validation.
            switch_text (str): Texte de changement de page (connexion <-> inscription)
            link_text (str): Texte de lien.
        """
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
 
        title_label, subtitle_label = make_header(title, subtitle)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(18)
 
        self.inputs: dict[str, QLineEdit] = {}
        self._password_inputs: list[QLineEdit] = []
 
        for spec in fields:
            field_label = QLabel(spec.label.upper())
            field_label.setObjectName("fieldLabel")
 
            edit = QLineEdit()
            edit.setPlaceholderText(spec.placeholder)
            if spec.is_password:
                edit.setEchoMode(QLineEdit.EchoMode.Password)
                self._password_inputs.append(edit)
 
            self.inputs[spec.key] = edit
            layout.addWidget(field_label)
            layout.addWidget(edit)
            layout.addSpacing(8)
 
        self.show_password: QCheckBox = QCheckBox("Afficher le mot de passe")
        self.show_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.show_password.toggled.connect(self._toggle_password)
        layout.addWidget(self.show_password)
        layout.addSpacing(14)
        self.message: QLabel = QLabel()
        self.message.setObjectName("messageLabel")
        self.message.setWordWrap(True)
        self.message.setTextFormat(Qt.TextFormat.RichText)
        self.message.hide()
        layout.addWidget(self.message)
        layout.addSpacing(10)
 
        self.submit_button: QPushButton = QPushButton(button_text)
        self.submit_button.setObjectName("primaryButton")
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.submit_button)
        layout.addSpacing(10)
 
        switch_row = QHBoxLayout()
        switch_row.addStretch()
        switch_row.addWidget(QLabel(switch_text))
        self.switch_button: QPushButton = QPushButton(link_text)
        self.switch_button.setObjectName("linkButton")
        self.switch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        switch_row.addWidget(self.switch_button)
        switch_row.addStretch()
        layout.addLayout(switch_row)
 
    def _toggle_password(self, visible: bool) -> None:
        mode = QLineEdit.EchoMode.Normal if visible else QLineEdit.EchoMode.Password
        for edit in self._password_inputs:
            edit.setEchoMode(mode)
            
    def show_message(self, text: str, hints: list[str] | None = None) -> None:
        html = f"<b>{text}</b>"
        if hints:
            html += "<br>" + "<br>".join(f"• {hint}" for hint in hints)
        self.message.setText(html)
        self.message.show()

    def clear_message(self) -> None:
        self.message.hide()