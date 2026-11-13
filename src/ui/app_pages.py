from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QWidget

from .gestion_user import GestionUserPage
from .add_product import AddProductPage
from .main_page import MainPage
from .auth_window import AuthWindow
from ..utils.csv_utils import Database


class AppWindow(QMainWindow):
    """Unique fenêtre de l'application : les pages sont empilées dedans."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Rackeur")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self._pages = {
            "main": (MainPage(self)),
            "add_product": (AddProductPage(self)),
            "gestion_user": (GestionUserPage(self)),
            "auth": (AuthWindow(self))
        }

        for page in self._pages.values():
            self.stack.addWidget(page)

    def switch_to(self, title_page: str) -> None:
        page = self._pages.get(title_page)

        if page is None:
            raise ValueError(f"Page inconnue : {title_page}")
        
        self.database = Database("catalogue.csv")
        if title_page in ("main", "gestion_user", "add_product"):
            page.database = Database("catalogue.csv")
            page.user_database = Database("utilisateurs.csv")
            page.refresh()

        self.stack.setCurrentWidget(page)
